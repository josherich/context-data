from django.contrib import admin
from .models import Page, Host

class PageAdmin(admin.ModelAdmin):
  readonly_fields = ('view_host_name',)
  fields = ['page_title', 'page_url', 'page_content', 'view_host_name', 'page_image']
  list_display = ('page_title', 'page_date', 'page_url', 'page_content', 'view_host_name', 'page_image', 'created_at')
  list_filter = ['created_at', 'page_host__host_name', 'page_host__host_category']
  search_fields = ['page_title','page_content']

  def view_host_name(self, obj):
    return obj.page_host.host_name
  view_host_name.empty_value_display = '???'
  view_host_name.short_description = 'Host Name'

class PageInline(admin.TabularInline):
  model = Page

class HostAdmin(admin.ModelAdmin):
  inlines = [PageInline,]
  fields = ['host_name', 'host_feed_url', 'host_category', 'host_lang']
  list_display = ('id' ,'host_name', 'host_feed_url', 'host_category', 'host_lang')
  list_filter = ['host_lang']
  empty_value_display = '-empty-'

admin.site.register(Page, PageAdmin)
admin.site.register(Host, HostAdmin)
