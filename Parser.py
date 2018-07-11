#!/usr/bin/python3

# should be able to sort by job title or posting dept
# should be able to filer by subset
import feedparser as fp
import re
from Post import Post
class Parser:

    working_posts = []

    def create_postings(self):
        post_list = []
        for entry in self.feed.entries:
            content = self.process_content(entry)
            post = Post(entry.title, entry.published, entry.updated, entry.author, content)
            post_list.append(post)

        return post_list

    def shorten_posting(self, t):
        return t[:150] + (t[150:] and '...')

    def process_content(self, entry):
        return self.remove_tags(entry.content[0].value)

    def remove_tags(self, raw):
        tagless = re.compile(r'<[^>]+>').sub('', raw)
        return tagless.replace('\n', '')

    def pretty_printer(self):
        for entry in self.working_posts:
            print("_____________________________________________")
            print("\t" + entry.title)
            print("\t\t" + self.shorten_posting(entry.content))
            print("\n\t" + entry.author)
            print("_____________________________________________")


    def handle_sort(self):
        print("What would you like to sort by, [J]ob title  or [D]epartment posted?")
        r = input("---> ")
        if(r == "j"):
            self.working_posts = sorted(self.working_posts, key=lambda entry: entry.title)
            self.pretty_printer()
        elif(r == "d"):
            self.working_posts = sorted(self.working_posts, key=lambda entry: entry.author)
            self.pretty_printer()
        else:
            print("An invalid option was selected. please try again.")

    def handle_filter(self):
        search_results = []
        print("What would you like to search?")
        query = input("---> ")
        print("What would you like to filter by, [J]ob title  or [D]epartment posted?")
        r = input("---> ")
        if(r == "j" or r == "d"):
            for entry in self.working_posts:
                if(r == "j" and query in entry.title):
                    search_results.append(entry)
                elif(r == "d" and query in entry.author):
                    search_results.append(entry)
            self.working_posts = search_results
            self.pretty_printer()
        else:
            print("An invalid option was selected. please try again.")

    def main(self):
        while True:
            print("What would you like to display?")
            print("[F]ilter postings, [A]ll postings, [S]ort, [Q]uit")
            re = input("---> ")
            if(re == "f"):
                self.handle_filter()
            elif(re == "s"):
                self.handle_sort();
            elif(re == "a"):
                self.working_posts = self.create_postings()
                self.pretty_printer()
            elif(re == "c"):
                self.pretty_printer()
            elif(re == "q"):
                quit()
            else:
                print("Didn't get meaningful input. Please try again.")

    def __init__(self):
        self.feed = fp.parse("https://www.jobsatosu.com/all_jobs.atom")
        self.working_posts = self.create_postings()
        self.main()

Parser()
