class TopicImage(object):
    """
    Class extract topic image
    """

    def __init__(self, url):
        req = requests.get(url)
        self.soup = BeautifulSoup(req.content, 'html.parser')
        self.tag = None
        self.items = []

    def find_image(self):
        """Parse and find topic image"""
        # Find divs containing wishlist items
        img_tags = self.soup.findAll(attrs={'tag': "img"})
        for img_tag in img_tags:
            src = item_tag['src']
            try:
                self.items.append(src)
            except TypeError:
                continue
        # item.attrMap['href']
        return self.items

class AsyncTopicImage(Wishlist):

    def __init__(self, url):
        self.url = url

    async def find_image(self):
        url = self.url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = await response.read()
        self.soup = BeautifulSoup(response, 'html.parser')
        self.tag = None
        self.items = []
        items = super(TopicImage, self).find_image()
        self.soup = None
        self.tag = None
        return items

def time_span(ts):
    '''
    '''
    delta = datetime.datetime.utcnow().replace(tzinfo=utc) - ts

    if delta.days >= 365:
        return '%d年前' % (delta.days / 365)

    elif delta.days >= 30:
        return '%d个月前' % (delta.days / 30)

    elif delta.days > 0:
        return '%d天前' % delta.days

    elif delta.seconds < 60:#www.iplaypython.com
        return "%d秒前" % delta.seconds

    elif delta.seconds < 60 * 60:
        return "%d分钟前" % (delta.seconds / 60)

    else:
        return "%d小时前" % (delta.seconds / 60 / 60)

def make_hash(obj):
    """Make a hash from an arbitrary nested dictionary, list, tuple or
    set.

    """
    if isinstance(obj, set) or isinstance(obj, tuple) or isinstance(obj, list):
        return hash(tuple([make_hash(e) for e in obj]))

    elif not isinstance(obj, dict):
        return hash(obj)

    new_obj = copy.deepcopy(obj)
    for k, v in new_obj.items():
        new_obj[k] = make_hash(v)

    return hash(tuple(frozenset(new_obj.items())))