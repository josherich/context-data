logger = logging.getLogger('mindynode_nltk.rss')

from mindynode_nltk.models import (
  Page,
  Host
)

from .utils.xml import parse_rss
import dateparser

def update_feeds(category='china'):
  for feed in Host.objects.filter(host_category=category):
    pages = parse_rss(feed.host_feed_url, feed.host_lang)
    if not pages:
      continue
    for page in pages:
      result = save_page(feed.id, page)
      logger.info('%s-%s' % (result, page['title']))

def save_page(feed_id, page_attr):
  '''
  page_attr {
    title:
    link:
    description:
    date:
  }
  '''
  host = Host.objects.get(pk=feed)
  try:
    page, created = host.page_set.get_or_create(page_url=page_attr['link'])
  except Page.MultipleObjectsReturned:
    return 'skip saving, previous error'
  if created:
    page.page_title = page_attr['title'] or "blank_title"
    page.page_date = dateparser.parse(page_attr['date'])
    page.page_content = page_attr['description'] or "blank_content"
    page.save(force_update=True)
    return 'done'
  else:
    return 'skip'