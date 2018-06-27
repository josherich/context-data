import logging
import requests
import xml.etree.ElementTree as ET
import lxml.html
from .opencc import convert_chinese

logger = logging.getLogger('mindynode_nltk.utils.xml')


def filter_page_stop_words(content):
  stop_words = ['钛媒体', '爱范儿', '#欢迎关注爱范儿官方微信公众号：爱范儿（微信号：ifanr），更多精彩内容第一时间为您奉上。', '原文链接', '查看评论', '新浪微博', '获取更多RSS：https://feedx.net']
  for word in stop_words:
    content = content.replace(word, '')
  return content

def request_xml(url, lang="en"):
  try:
    response = requests.request('GET', url, timeout=25)
    if lang in ['zh_gb']:
      response.encoding = 'gb2312'
      text = response.text.replace("encoding=\"gb2312\"?>","encoding=\"utf-8\"?>")
    else:
      response.encoding = 'utf-8'
      text = response.text
  except requests.exceptions.Timeout:
    return False
  try:
    result = ET.fromstring(text)
  except ET.ParseError:
    return False
  return result

def parse_rss(url, lang):
  xml = request_xml(url, lang)
  if not xml:
    return []
  result = []
  for node in xml.iter('item'):
    try:
      title = node.find('title').text
      link = node.find('link').text
      has_date = node.find('pubDate')

      if has_date is None:
        logger.error('pubDate missing: %s' % (url))

      date = has_date.text if has_date is not None else ""
      content = node.find('description').text or ""
      content = lxml.html.document_fromstring(content).text_content()
    except lxml.etree.XMLSyntaxError:
      logger.error('xml syntax error: %s' % (node.find('link').text))
      continue
    except lxml.etree.ParserError:
      logger.error('xml parsing error: %s' % (node.find('link').text))
      continue
    if lang in ['zh_hk', 'zh_tw']:
      title = convert_chinese(title)
      content = convert_chinese(content)
    content = filter_page_stop_words(content)
    result.append({
      'title': title or content,
      'link': link,
      'description': content,
      'date': date
    })
  return result