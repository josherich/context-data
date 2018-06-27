#coding:utf-8

from __future__ import unicode_literals

from django.db import models
from mindynode_service.fulltext import SearchManager

class Page(models.Model):
  '''
  文章
  '''
  objects = SearchManager(['page_title', 'page_content'])
  page_title = models.CharField(verbose_name="标题", null=True, default="无标题", max_length=255)
  page_url = models.CharField(verbose_name="url", null=True, default="", max_length=255)
  page_content = models.TextField(verbose_name="内容", null=False, blank=False, max_length=10000 )
  page_date = models.CharField(verbose_name="pubDate", null=True, default="", max_length=255)
  page_host = models.ForeignKey('Host', on_delete=models.CASCADE)
  page_image = models.CharField(verbose_name="图片url", null=True, default="", max_length=255)
  page_topics = models.CharField(verbose_name="tdidf词", null=True, default="", max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'page_entity'
    verbose_name = 'PageEntities'
    verbose_name_plural = verbose_name
    
class Host(models.Model):
  '''
  媒体
  '''
  host_name = models.CharField(verbose_name="媒体名", null=True, default="无标题", max_length=255)
  host_desc = models.CharField(verbose_name="媒体描述", null=True, default="无标题", max_length=255)
  host_category = models.CharField(verbose_name="类别", null=True, default="默认", max_length=255)
  host_homepage = models.CharField(verbose_name="主页", null=True, default="", max_length=255)
  host_feed_url = models.CharField(verbose_name="主页", null=True, default="", max_length=255)
  host_icon = models.CharField(verbose_name="图标", null=True, default="", max_length=255)
  host_corp_id = models.CharField(verbose_name="节点", null=True, default="", max_length=255)
  host_info = models.CharField(verbose_name="节点", null=True, default="", max_length=255)
  host_lang = models.CharField(verbose_name="语言", null=True, default="zh", max_length=255)

  class Meta:
    db_table = 'media_entity'
    verbose_name = 'MediaEntities'
    verbose_name_plural = verbose_name

""" deprecated models """
"""  """
"""  """
"""  """
"""  """
class KeywordSum(models.Model):
  '''
  带权关键词
  '''
  keyword_name = models.CharField(verbose_name="中文名", default=None, max_length=255)
  keyword_pos = models.CharField(verbose_name="POS", default=None, max_length=255)
  keyword_cal_date = models.DateTimeField(verbose_name="计算事件", null=True, default=None)
  keyword_weight = models.FloatField(verbose_name="权重", default=0)
  keyword_source = models.CharField(verbose_name="来源", null=True, default=None, max_length=255)
  keyword_image = models.CharField(verbose_name="图片url", null=True, default="", max_length=255)
  keyword_category = models.CharField(verbose_name="类别", null=True, default="china", max_length=255)
  keyword_time_type = models.CharField(verbose_name="时间类别", null=True, default="time", max_length=255)

  class Meta:
    db_table = 'feed_keywords_sum'
    verbose_name = 'KeywordSum'
    verbose_name_plural = verbose_name

class FeedKeywords(models.Model):
  '''
  关键词
  '''
  keyword_name = models.CharField(verbose_name="中文名", null=True, default=None, max_length=255)
  keyword_pos = models.CharField(verbose_name="POS", null=True, default=None, max_length=255)
  keyword_start_date = models.DateTimeField(verbose_name="开始计算时间", null=True, default=None)
  keyword_weight = models.FloatField(verbose_name="权重", default=0 )
  keyword_source = models.CharField(verbose_name="来源", null=True, default=None, max_length=255)
  keyword_page = models.ForeignKey('Page', on_delete=models.CASCADE)

  class Meta:
    db_table = 'feed_keywords'
    verbose_name = 'FeedKeywords'
    verbose_name_plural = verbose_name

class NounPhrase(models.Model):
  '''
  词组
  '''
  np_name = models.CharField(verbose_name="中文名", null=True, default=None, max_length=255)
  np_json = models.CharField(verbose_name="源数组", null=True, default=None, max_length=255)
  np_page = models.ForeignKey('Page', on_delete=models.CASCADE)
  np_source = models.CharField(verbose_name="来源", null=True, default=None, max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'noun_phrases'
    verbose_name = 'NounPhrase'
    verbose_name_plural = verbose_name

class BOW(models.Model):
  '''
  BOW for daily model
  '''
  bow_words = models.CharField(verbose_name="关键词数组", null=True, default="today", max_length=10000)
  bow_category = models.CharField(verbose_name="类别", null=True, default="today", max_length=255)
  bow_visible = models.BooleanField(verbose_name="已审核", null=False, default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'bow_entity'
    verbose_name = 'BOWEntity'
    verbose_name_plural = 'BOWEntities'

class TrendWord(models.Model):
  '''
  Trending keywords for daily model
  '''
  trend_words = models.CharField(verbose_name="关键词名", null=True, default="untitle", max_length=255)
  trend_count = models.IntegerField(verbose_name="词频",default=1)
  trend_category = models.CharField(verbose_name="类别", null=True, default="china", max_length=255)
  trend_visible = models.BooleanField(verbose_name="已审核", null=False, default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'trend_entity'
    verbose_name = 'TrendEntity'
    verbose_name_plural = 'TrendEntities'

class PageGroup(models.Model):
  '''
  文章聚类集合
  '''
  group_id = models.CharField(verbose_name="主页面id", null=True, default="", max_length=255)
  group_json = models.TextField(verbose_name="data json", null=False, blank=False, max_length=10000 )
  group_type = models.CharField(verbose_name="时间类型", null=True, default="today", max_length=255)
  group_length = models.IntegerField(verbose_name="聚类长度",default=1)
  group_pages = models.ManyToManyField(Page)
  group_category = models.CharField(verbose_name="内容类别", null=True, default="china", max_length=255)
  group_topics = models.CharField(verbose_name="主题词", null=True, default="", max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'page_group_entity'
    verbose_name = 'PageGroupEntity'
    verbose_name_plural = 'PageGroupEntities'

class StopWord(models.Model):
  '''
  自定义停用词
  '''
  stopword_name = models.CharField(verbose_name="词名", null=True, default="无标题", max_length=255)
  stopword_category = models.CharField(verbose_name="类别名", null=True, default="general", max_length=255)
  stopword_weight = models.FloatField(verbose_name="权重", default=0)
  class Meta:
    db_table = 'stop_word'
    verbose_name = 'StopWord'
    verbose_name_plural = verbose_name