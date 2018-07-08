#!/usr/bin/python

import feedparser as fp
import re

class Parser:

    def print_the_thing(self):
        print(self.feed.feed.title)
        print()
        for entry in self.feed.entries:
            t = self.process_content(entry)
            print("\t" + entry.title)
            # if a job description is absurdly long, chops the string and adds elipsies
            print("\t\t" + t[:150] + (t[150:] and '...'))
            print()

    def process_content(self, entry):
        return self.remove_tags(entry.content[0].value)

    def remove_tags(self, raw):
        tagless = re.compile(r'<[^>]+>').sub('', raw)
        return tagless.replace('\n', '')

    def __init__(self):
        self.feed = fp.parse("https://www.jobsatosu.com/all_jobs.atom")
        self.print_the_thing()

Parser()
