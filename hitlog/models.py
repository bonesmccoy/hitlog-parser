from collections import namedtuple

ArticleEntry = namedtuple('ArticleEntry', 'page_name page_url')


class PageHit:

    def __init__(self, page_name, page_url, user_id, timestamp):
        self.page = Page(page_name, page_url)
        self.user_id = user_id
        self.timestamp = int(timestamp)

    def __repr__(self):
        return "{}, {}, {}".format(self.page, self.user_id, self.timestamp)


class Page:

    REGISTRATION_TOKEN = '/register'
    ARTICLE_TOKEN = '/articles/'

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def is_article(self):

        return self.ARTICLE_TOKEN in self.url

    def is_register(self):
        return self.REGISTRATION_TOKEN in self.url

    def __repr__(self):

        return "{} {}".format(self.name, self.url)


class Hit:

    def __init__(self, page, user_id, timestamp):

        self.page = page
        self.user_id = int(user_id)
        self.timestamp = int(timestamp)

