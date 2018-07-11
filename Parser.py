#!/usr/bin/python3

import feedparser as fp
import re
from Post import Post
from datetime import datetime
import webbrowser
class Parser:

    working_posts = []

    # Refreshes working posts
    def create_postings(self):
        post_list = []
        for entry in self.feed.entries:
            content = self.process_content(entry)
            post = Post(entry.title, entry.published_parsed, entry.updated_parsed, entry.author, content, entry.link, len(post_list))
            post_list.append(post)
        return post_list

    def is_int(self, t):
        try:
            int(t)
            return True
        except ValueError:
            return False

    def shorten_posting(self, t):
        return t[:150] + (t[150:] and '...')

    def process_content(self, entry):
        return self.remove_tags(entry.content[0].value)

    def remove_tags(self, raw):
        tagless = re.compile(r'<[^>]+>').sub('', raw)
        return tagless.replace('\n', '')

    def parse_datetime(self, dt):
        return datetime.strftime(dt, "%m/%d/%y at %H:%M")

    def pretty_printer(self, to_print):
        if len(to_print) > 0:
            for entry in to_print:
                self.print_entry(True, entry)
        else:
            print("** No result to display. **")

    def print_entry(self, shorten, entry):
        print("--------------------------------------------")
        print("\n\t" + str(entry.id) + ": " + entry.title)
        if shorten:
             print("\n\t\t" + self.shorten_posting(entry.content))
        else:
            print("\n\t\t" + entry.content)
        print("\n\t" + entry.author)
        print("\n---------------------------------------------")
        print("\tCreated at " + self.parse_datetime(entry.published))
        print("\tLast updated at " + self.parse_datetime(entry.updated))

    def open_in_browser(self, entry):
        print("Would you like to open the link to the posting? Enter y to open the link, or any other key to return to the main menu.")
        r = input("---> ")
        if(r == "y"):
            webbrowser.open(entry.link)

    def handle_sort(self):
        print("What would you like to sort by, [J]ob title  or [D]epartment posted?")
        r = input("---> ")
        if(r == "j"):
            self.working_posts = sorted(self.working_posts, key=lambda entry: entry.title)
            self.pretty_printer(self.working_posts)
        elif(r == "d"):
            self.working_posts = sorted(self.working_posts, key=lambda entry: entry.author)
            self.pretty_printer(self.working_posts)
        else:
            print("An invalid option was selected. Please try again.")

    def handle_filter(self):
        search_results = []
        print("What would you like to search?")
        query = input("---> ")
        print("What would you like to filter by, [J]ob title  or [D]epartment posted?")
        r = input("---> ")
        if(r == "j" or r == "d"):
            for entry in self.working_posts:
                if(r == "j" and query in entry.title) or (r == "d" and query in entry.author):
                    search_results.append(entry)
            self.working_posts = search_results
            self.pretty_printer(self.working_posts)
        else:
            print("An invalid option was selected. please try again.")

    def view_post(self):
        while True:
            print("Which post ID would you like to view in more detail?")
            r = input("---> ")
            if self.is_int(r) and int(r) < len(self.working_posts):
                for entry in self.working_posts:
                    if entry.id == int(r):
                        self.print_entry(False, entry)
                        self.open_in_browser(entry)
                        return
            print("An invalid ID was chosen. Please try again.")

    def main(self):
        while True:
            print("+"*169)
            print("\nWhat would you like to display?\n")
            print("[F]ilter postings, [A]ll postings, [E]xamine posting, [S]ort, [Q]uit")
            re = input("*---> ")
            if(re == "f"):
                self.handle_filter()
            elif(re == "s"):
                self.handle_sort();
            elif(re == "a"):
                self.working_posts = self.create_postings()
                self.pretty_printer(self.working_posts)
            elif(re == "c"):
                self.pretty_printer(self.working_posts)
            elif(re == "q"):
                quit()
            elif(re == "e"):
                self.view_post()
            else:
                print("Didn't get meaningful input. Please try again.")

    def __init__(self):
        self.feed = fp.parse("https://www.jobsatosu.com/all_jobs.atom")
        self.working_posts = self.create_postings()
        self.main()

Parser()
