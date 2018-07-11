#!/usr/bin/python3

class Post(object):
    title = ''

    # change this to datetime later
    published = ''
    updated = ''

    author = ''
    content = ''

    # stretch goal: add link to original job posting in the object
    def __init__(self, title, published, updated, author, content):
        self.title = title
        self.published = published
        self.updated = updated
        self.author = author
        self.content = content

    def make_post(title, published, updated, author, content):
        return Post(title, published, updated, author, content)
