from bs4 import BeautifulSoup
from .xml import request_xml

def google_news(query, locale):
  uri = "https://news.google.com/news/rss/explore/section/q/%s?ned=%s&hl=#%s" % (query, locale, locale)
  list = request_xml(uri)
  result = []
  if not list:
    return []
  for node in list.iter('item'):
    content = node.find('description').text or ""
    date = node.find('pubDate').text
    pages = _parse_google_news(content, date)
    result.extend(pages)
  return result

def _parse_google_news(html, date):
  soup = BeautifulSoup(html, 'html.parser')
  list = soup.find_all('li')
  image = soup.find('img')
  return [{
    "title": item.find('a').text,
    "url": item.find('a')['href'],
    "host": item.find('font').text,
    "content": "",
    "created_at": date,
  } for item in list]