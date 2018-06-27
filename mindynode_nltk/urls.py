from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^pages/search$',      views.api_search_pages,         name='api_search_pages'),
  url(r'^pages/search/date$', views.api_search_pages_by_date, name='api_search_pages_by_date'),
  url(r'^pages/count$',       views.api_search_pages_count,   name='api_search_pages_count'),
  
  url(r'^pages/section$',        views.api_get_pages_for_category, name='api_get_pages_for_category'),
  url(r'^pages/media$',        views.api_get_pages_for_host, name='api_get_pages_for_host'),

  url(r'^words/recent$',        views.api_get_words_recent, name='api_get_words_recent'),

  url(r'^timeline/search$', views.api_search_timeline,  name='api_search_timeline'),
  url(r'^rss/search$',      views.api_search_rss,       name='api_search_rss'),
  url(r'^googlenews/search$', views.api_search_google_news, name='api_search_google_news'),
  
  url(r'^sections', views.api_get_categories, name='api_get_categories'),
  url(r'^media', views.api_get_hosts, name='api_get_hosts'),

  url(r'^nlp/reference$', views.api_get_reference, name='api_get_reference'),
]