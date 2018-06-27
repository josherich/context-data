from gensim import corpora, models, similarities
from mindynode_nltk.models import Page, PageGroup, TrendWord
from .nltk import noun_phrases_zh, noun_phrases_en
from datetime import datetime, date, time, timedelta
from itertools import groupby

import operator
import json
import math
import gc

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger('mindynode_nltk.utils.vectors')

model_cof = 0.25
today_range = 24

# filter_extremes(no_below=5, no_above=0.5, keep_n=100000, keep_tokens=None)

def build_dictionary(lang='zh'):
  texts = []
  if lang == 'zh':
    pages = Page.objects.filter(page_host__host_lang__in=['zh', 'zh_hk', 'zh_gb']).order_by('created_at')
  elif lang == 'en':
    pages = Page.objects.filter(page_host__host_lang='en').order_by('created_at')

  for page in pages:
    texts.append([word.keyword_name for word in page.feedkeywords_set.all()])
  dictionary = corpora.Dictionary(texts)
  dictionary.save('lib/dict-{}.dict'.format(lang))

def update_dictionary(lang='zh'):
  texts = []
  start_day = datetime.combine(date.today(), time()) - timedelta(hours=today_range)

  if lang == 'zh':
    pages = Page.objects.filter(page_host__host_lang__in=['zh', 'zh_hk', 'zh_gb'], created_at__gt=start_day).order_by('created_at')
  elif lang == 'en':
    pages = Page.objects.filter(page_host__host_lang='en', created_at__gt=start_day).order_by('created_at')

  for page in pages:
    texts.append([word.keyword_name for word in page.feedkeywords_set.all()])

  dictionary = corpora.Dictionary.load('lib/dict-{}.dict'.format(lang))
  dictionary.add_documents(texts)
  dictionary.save('lib/dict-{}.dict'.format(lang))
  dictionary = None

def build_today_index(category='china', lang='zh'):
  logger.info('enter build today index')
  start_day = datetime.combine(date.today(), time()) - timedelta(hours=today_range)
  pages = Page.objects.filter(page_host__host_category=category, created_at__gt=start_day).order_by('created_at')

  texts = []
  for page in pages:
    text = [word.keyword_name for word in page.feedkeywords_set.all()]
    if len(text) == 0:
      text = ['默认']
    texts.append(text)
  dictionary = corpora.Dictionary.load('lib/dict-{}.dict'.format(lang))
  corpus = [dictionary.doc2bow(text) for text in texts]
  corpora.MmCorpus.serialize('lib/today-corpus-{}.mm'.format(category), corpus)
  dictionary = None
  corpus = None

def build_today_bow(category='china', lang='zh', N=100):
  dictionary = corpora.Dictionary.load('lib/dict-{}.dict'.format(lang))
  start_day = datetime.combine(date.today(), time()) - timedelta(hours=today_range)
  pages = Page.objects.filter(page_host__host_category=category, created_at__gt=start_day).order_by('created_at')
  texts = [(word.keyword_name, word.keyword_pos) for page in pages for word in page.feedkeywords_set.all()]

  if lang == 'zh':
    texts = [tp[0] for tp in texts if tp[1] != 'n']
  else:
    texts = [tp[0] for tp in texts]

  bow = [(dictionary.get(word[0]), word[1]) for word in sorted(dictionary.doc2bow(texts), key=lambda tp: -tp[1])[0:N]]
  TrendWord.objects.bulk_create([
    TrendWord(
      trend_words=word[0],
      trend_count=word[1],
      trend_category=category
    ) for word in bow])

def build_today_model(category='china', lang='zh'):
  logger.info('enter build today model')
  start_day = datetime.combine(date.today(), time()) - timedelta(hours=today_range)
  count = Page.objects.filter(page_host__host_category=category, created_at__gt=start_day).count()

  dictionary = corpora.Dictionary.load('lib/dict-{}.dict'.format(lang))
  corpus = corpora.MmCorpus('lib/today-corpus-{}.mm'.format(category))
  lsi = models.LsiModel(corpus, chunksize=2000, id2word=dictionary, num_topics=math.floor(count * model_cof))
  index = similarities.MatrixSimilarity(lsi[corpus])
  index.save('lib/today-lsi-{}.index'.format(category))
  lsi.save('lib/today-{}.lsi'.format(category))
  dictionary = None
  corpus = None
  lsi = None
  index = None

def _group_pages(pages, simi_func, dictionary, lsi, index, category, lang):
  group_dict = {}
  duplicate_dict = {}
  for page in pages:
    word_vec = [word.keyword_name for word in page.feedkeywords_set.all()]
    sims = simi_func(word_vec, dictionary, lsi, index, category, lang)
    for id, value in sims:
      if id in duplicate_dict:
        continue
      simi_page = Page.objects.get(id=id)
      duplicate_dict[id] = page.id
      group_dict['{}:{}'.format(id, value)] = page.id
  result_dict = {}
  for key, value in group_dict.items():
    if value in result_dict:
      result_dict[value].append(key)
    else:
      result_dict[value] = [key]
  return result_dict

def group_today_pages(category='china', lang='zh'):
  logger.info('enter group today pages')
  start_day = datetime.combine(date.today(), time()) - timedelta(hours=today_range)
  pages = Page.objects.filter(page_host__host_category=category, created_at__gt=start_day).order_by('created_at')

  dictionary = corpora.Dictionary.load('lib/dict-{}.dict'.format(lang))
  lsi = models.LsiModel.load('lib/today-{}.lsi'.format(category))
  index = similarities.MatrixSimilarity.load('lib/today-lsi-{}.index'.format(category))

  result_dict = _group_pages(pages, query_today_simi, dictionary, lsi, index, category, lang)

  dictionary = None
  lsi = None
  index = None

  PageGroup.objects.filter(group_type='today', group_category=category).delete()
  for key, value in result_dict.items():
    if len(value) > 1:
      group = PageGroup.objects.create(
        group_id=key,
        group_json=json.dumps(value),

        group_length=len(value),
        group_type='today',
        group_category=category
      )
      ids = [p.split(':')[0] for p in value]
      pages = Page.objects.filter(pk__in=ids)
      group.group_pages = pages
      group.group_topics = ','.join(page_topics_topN(pages))
      group.save()


def page_topics_topN(pages):
  result = {}
  words = [word for page in pages for word in page.page_topics.split(',')]
  for key, value in groupby(words):
    result[key] = len(list(value))
  sorted_words = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
  return [tp[0] for tp in sorted_words[0:8]]

def build_history_index(category='china', lang='zh'):
  pages = Page.objects.filter(page_host__host_category=category).order_by('created_at')

  texts = []
  for page in pages:
    text = [word.keyword_name for word in page.feedkeywords_set.all()]
    if len(text) == 0:
      text = ['默认']
    texts.append(text)
  dictionary = corpora.Dictionary.load('lib/dict-{}.dict'.format(lang))
  corpus = [dictionary.doc2bow(text) for text in texts]
  corpora.MmCorpus.serialize('lib/history-corpus-{}.mm'.format(category), corpus)

def group_history_pages(category='china', lang='zh'):
  start_day = datetime.combine(date.today(), time()) - timedelta(hours=24*90)
  pages = Page.objects.filter(page_host__host_category=category, created_at__gt=start_day).order_by('created_at')

  dictionary = corpora.Dictionary.load('lib/dict-{}.dict'.format(lang))
  lsi = models.LsiModel.load('lib/history-{}.lsi'.format(category))
  index = similarities.MatrixSimilarity.load('lib/history-lsi-{}.index'.format(category))

  result_dict = _group_pages(pages, query_history_simi, dictionary, lsi, index, category, lang)
  PageGroup.objects.filter(group_type='history', group_category=category).delete()
  for key, value in result_dict.items():
    group = PageGroup.objects.create(
      group_id=key,
      group_json=json.dumps(value),

      group_length=len(value),
      group_type='history',
      group_category=category
    )
    ids = [p.split(':')[0] for p in value]
    pages = Page.objects.filter(pk__in=ids)
    group.group_pages = pages
    group.group_topics = ','.join(page_topics_topN(pages))
    group.save()

def build_history_model(category='china', lang='zh'):
  dictionary = corpora.Dictionary.load('lib/dict-{}.dict'.format(lang))
  corpus = corpora.MmCorpus('lib/history-corpus-{}.mm'.format(category))
  lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=200)
  index = similarities.MatrixSimilarity(lsi[corpus])
  index.save('lib/history-lsi-{}.index'.format(category))
  lsi.save('lib/history-{}.lsi'.format(category))

def query_history_simi(word_vec, dictionary, lsi, index, category='china', lang='zh'):
  vec_bow = dictionary.doc2bow(word_vec)
  vec_lsi = lsi[vec_bow]
  sims = index[vec_lsi]
  sims = sorted(enumerate(sims), key=lambda item: -item[1])
  event = list(filter(lambda x: x[1] > 0.9, sims))
  # start_day = datetime.combine(date.today(), time()) - timedelta(days=180)
  pages = Page.objects.filter(page_host__host_category=category).order_by('created_at')
  return [(pages[sim[0]].id, sim[1]) for sim in event]

def query_today_simi(word_vec, dictionary, lsi, index, category='china', lang='zh'):
  vec_bow = dictionary.doc2bow(word_vec)
  vec_lsi = lsi[vec_bow]
  sims = index[vec_lsi]
  sims = sorted(enumerate(sims), key=lambda item: -item[1])
  event = list(filter(lambda x: x[1] > 0.9, sims))
  start_day = datetime.combine(date.today(), time()) - timedelta(hours=today_range)
  pages = Page.objects.filter(page_host__host_category=category, created_at__gt=start_day).order_by('created_at')
  return [(pages[sim[0]].id, sim[1]) for sim in event]

def build_history_pages(category, lang):
  build_history_index(category, lang)
  build_history_model(category, lang)

def build_today_pages(category, lang):
  update_dictionary(lang)
  build_today_index(category, lang)
  build_today_model(category, lang)
  gc.collect()
