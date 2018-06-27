import re
import math
import json
import logging
import requests

import urllib.parse
import functools

from django.db.models import Q
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, date, time, timedelta

from .utils.google_news import google_news
from .utils.helper import days_ago
from .utils.xml import parse_rss
import dateparser

from mindynode_nltk.models import (
  Page,
  Host
)

SECTION_MAP = {
  'china': '所有',
  'zh_tech': '科技',
  'zh_economics': '经济',
  'zh_life': '生活',
  'zh_world': '世界',
  'zh_sports': '体育',
  'zh_opinion': '意见',
  'zh_politics': '政治',

  'en_business': 'business',
  'en_economics': 'economics',
  'en_life': 'life',
  'en_politics': 'politics',
  'en_sports': 'sports',
  'en_tech': 'technology',
  'en_general': 'general'
}

logger = logging.getLogger('mindynode_nltk.functions')

def search_pages(words, category='china'):
  pages = Page.objects.search(words) \
  .select_related('page_host') \
  .order_by('-created_at') \
  .only('page_title', 'page_content', 'page_url', 'page_image', 'created_at', 'page_host')
  return {
    "pages": [{
      "title": page.page_title,
      "content": page.page_content,
      "host": page.page_host.host_name,
      "url": page.page_url,
      "image": page.page_image,
      "created_at": page.created_at
    } for page in pages[:20]]
  }

def search_timeline(words, category='china'):
  pages = Page.objects.search(words)
  date_title_pair = {}
  for page in pages:
    date = page.created_at.strftime('%Y-%m-%d')
    if date in date_title_pair:
      date_title_pair[date].append(page.page_title)
    else:
      date_title_pair[date] = [page.page_title]
  return { "pages": date_title_pair }

def search_rss(words, category='china'):
  pages = Page.objects.search(words) \
    .select_related('page_host') \
    .order_by('-created_at') \
    .only('page_title', 'page_content', 'page_url', 'created_at', 'page_host')
  return {
    "pages": [{
      "title": page.page_title,
      "content": page.page_content,
      "host": page.page_host.host_name,
      "url": page.page_url,
      "created_at": page.created_at
    } for page in pages[:20]]
  }

def search_google_news(keyword="trump", lang="us"):
  return google_news(keyword, lang)

def search_pages_by_date(words, date, category='china'):
  start_date = datetime.strptime(date, '%Y-%m-%d')
  pages = Page.objects.search(words).filter(created_at__range=(start_date,start_date+timedelta(hours=24)))
  return [{
    "title": page.page_title,
    "content": page.page_content,
    "url": page.page_url,
    "image": page.page_image,
    "host": page.page_host.host_name,
    "created_at": page.created_at
  } for page in pages]

def search_pages_count(words, date):
  start_date = datetime.strptime(date, '%Y-%m-%d')
  pages = Page.objects.search(words).filter(created_at__gt=start_date)
  return pages.count()

def get_pages_for_category(days=1, category='china', limit=20):
  start_date = days_ago(days)
  # end_date = start_date + timedelta(hours=24)
  hosts = Host.objects.filter(host_category=category)
  return [{
    'title': page.page_title,
    'url': page.page_url,
    'content': page.page_content,
    'host': page.page_host.host_name,
    'count': host.page_set.filter(created_at__gt=start_date).count()
  } for host in hosts for page in host.page_set.filter(created_at__gt=start_date).order_by('-created_at')[:limit]]

def get_pages_for_host(days=1, host='', limit=20):
  start_date = days_ago(days)
  hosts = Host.objects.filter(host_name=host)
  return [{
    'title': page.page_title,
    'url': page.page_url,
    'content': page.page_content,
    'host': page.page_host.host_name,
  } for host in hosts for page in host.page_set.filter(created_at__gt=start_date).order_by('-created_at')[:limit]]

def get_hosts(category='china'):
  hosts = Host.objects.filter(host_category=category)
  return [{
    'name': host.host_name,
    'desc': host.host_desc,
    'homepage': host.host_homepage,
    'feed_url': host.host_feed_url,
    'icon_url': host.host_icon,
  } for host in hosts]

def get_categories():
  hosts = Host.objects.all()
  categories = set([host.host_category for host in hosts])
  return [{
      "id": SECTION_MAP[cate],
      "name": cate
    } for cate in categories]

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
  host = Host.objects.get(pk=feed_id)
  try:
    page, created = host.page_set.get_or_create(page_url=page_attr['link'])
  except Page.MultipleObjectsReturned:
    return 'skip saving, previous error'
  if created:
    page.page_title = page_attr['title'] or "blank_title"
    page.page_date = dateparser.parse(page_attr['date'])
    # page.page_date = page_attr['date']
    print(page.page_date)
    page.page_content = page_attr['description'] or "blank_content"
    page.save(force_update=True)
    return 'done'
  else:
    return 'skip'