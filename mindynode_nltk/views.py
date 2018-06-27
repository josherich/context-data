#coding:utf-8

from __future__ import unicode_literals
from __future__ import division

import re
import json
from datetime import datetime, date, time, timedelta

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

from mindynode_nltk.functions import *
# from .tasks import task_update_feeds

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_search_pages(request):
  data = json.loads(request.body.decode('utf-8'))
  response = JsonResponse({ 'data': search_pages(data['keywords'], data['category'])})
  return response

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_search_pages_by_date(request):
  data = json.loads(request.body.decode('utf-8'))
  response = JsonResponse({ 'data': { 'pages': search_pages_by_date(data['keywords'] , data['date'], data['category'])}})
  return response

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_search_pages_count(request):
  data = json.loads(request.body.decode('utf-8'))
  result = search_pages_count(data['words'], data['date'])
  response = JsonResponse({ 'data': result })
  return response

@require_http_methods(["GET"])
def api_get_pages_for_category(request):
  days = request.GET.get('days', 0)
  category = request.GET.get('category', 'china')
  response = JsonResponse({ 
    'data': get_pages_for_category(int(days), category) 
  })
  return response

@require_http_methods(["GET"])
def api_get_pages_for_host(request):
  name = request.GET.get('host', '')
  days = request.GET.get('days', 100)
  response = JsonResponse({
    'data': get_pages_for_host(int(days), name)
  })
  return response


@require_http_methods(["GET"])
def api_get_words_recent(request):
  lang = request.GET.get('lang', 'cn')
  response = JsonResponse({
    'data': ["+特朗普+朝鲜", "+纪委+处分", "+英国", "+俄罗斯", "+墨西哥", "+香港", "+联合国", "+河北", "+伦敦", "+印度", "+昂山素季", "+成都", "+澳门", "+中央军委", "+联合国大会", "+韩国"]
  })
  return response

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_search_timeline(request):
  data = json.loads(request.body.decode('utf-8'))
  response = JsonResponse({ 'data': search_timeline(data['keywords'], data['category'])})
  return response

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_search_rss(request):
  data = json.loads(request.body.decode('utf-8'))
  response = JsonResponse({ 'data': search_rss(data['keywords'], data['category'])})
  return response

@require_http_methods(["GET"])
def api_search_google_news(request):
  query = request.GET.get('query', "")
  lang = request.GET.get('lang', 'zh')
  response = JsonResponse({ 'data': search_google_news(query, lang) })
  return response

@require_http_methods(["GET"])
def api_get_hosts(request):
  section = request.GET.get('section', 'china')
  response = JsonResponse({
    'data': get_hosts(section)
  })
  return response

@require_http_methods(["GET"])
def api_get_categories(request):
  response = JsonResponse({
    'data': get_categories()
  })
  return response

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_get_reference(request):
  result = extract_reference(request.body.decode('utf-8'))
  response = JsonResponse(result)
  return response