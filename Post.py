#!/usr/bin/python3

from datetime import datetime
from time import mktime

class Post(object):
    title = ''

    published = ''
    updated = ''

    author = ''
    content = ''
    link = ''
    id = 0

    def __init__(self, title, published, updated, author, content, link, id):
        self.title = title
        self.published = self.parse_dates(published)
        self.updated = self.parse_dates(updated)
        self.author = author
        self.content = content
        self.id = id
        self.link = link

    def parse_dates(self, date):
        return datetime.fromtimestamp(mktime(date))
