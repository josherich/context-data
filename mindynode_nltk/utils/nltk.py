
def find_reference(content):
  query = re.compile('(\(\S+[\,\，]\s?\d{4}\))')
  return re.findall(query, content)