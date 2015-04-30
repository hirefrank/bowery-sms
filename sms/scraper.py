#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Scrape the daily workouts from Bowery CrossFit blog's sitemap.
URL = 'http://www.bowerycrossfit.com/post-sitemap.xml'

try:
    from settings_local import *
except ImportError as e:
    from settings import *

import requests
import bs4
import re
import unicodedata

from HTMLParser import HTMLParser

from parse_rest.connection import register
from parse_rest.datatypes import Object, ACL

# Common abbreviations to help reduce the text message length.
abbreviations = {
    'minutes': 'min',
    'seconds': 'sec',
    'meters': 'm',
    'Chest-to-Bar': 'CTB',
    'Chest to Bar': 'CTB',
    'Pull-Ups': 'PU',
    'Pull Ups': 'PU',
    'as many rounds and reps as possible': 'AMRAP',
    'as many rounds as possible': 'AMRAP',
    'as many reps as possible': 'AMRAP',
    'back squat': 'BS',
    'hang squat clean': 'HSC',
    'hang clean': 'HC',
    'clean and jerk': 'C&J',
    'every minute on the minute': 'EMOM',
    'front squat': 'FS',
    'hand stand push up': 'HSPU',
    'knees to elbow': 'KTE',
    'muscle ups': 'MU',
    'overhead squat': 'OHS',
    'power clean': 'PC',
    'push press': 'PP',
    'push-press': 'PP',
    'push jerk': 'PJ',
    'power snatch': 'PSN',
    'squat clean': 'SC',
    'sumo deadlift high pull': 'SDHP',
    'toes to bar': 'TTB',
    'push-ups': 'PU',
    'snatch': 'SN',
    'squat': 'SQ',
    'kettlebell': 'KB',
    'clean': 'CLN',
    'deadlift': 'DL',
    ' one': ' 1',
    ' two': ' 2',
    ' three': ' 3',
    ' four': ' 4',
    ' five': ' 5',
    'rounds for time of': 'RFT',
    'rounds for time': 'RFT',
    'alternating': 'alt',
    'sit-ups': 'SU',
    'Sit-Ups': 'SU',
    'Double-Unders': 'DU',
    }

# This is ugly. I should do this better.
# Todo: Actually learn about encoding.
special_chars = {
    '’': "'",
    '‘': "'",
    '“': '"',
    '”': '"',
    '…': '...',
    '\xc2\xa0' : ' ',
    }

# Possible headers
headers = {
    'Open Workout:': 'Experienced Workout:',
    'Experienced Level:': 'Open Level:',
    'Experienced/Open': None,
    'Workout:': None,
    #':': None, # catchall sort of hacky
    }

class Workout(Object):
    pass

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_programming_urls():
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text)

    # reverse to get the most recent urls first
    urls = list(reversed([url.text for url in soup.findAll("loc")]))

    # limit to last 5 urls
    del urls[5:]

    # reverse on return to process in asc order
    return reversed(urls)

def has_wod(content):
    if not "Open gym" in content:
        return True
    else:
        return False

def clean_content(content):
    # loop through each possible header
    match = False
    for key in headers:
        if key in content:
            match = True
            # if testing week
            if 'Testing week!' in content:
                clean = re.sub('Testing week!.*?' + key,'', strip_tags(content.replace("</p>", "</p> ")), flags=re.DOTALL)
            else:
                clean = re.sub('Recommended content:.*?' + key,'', strip_tags(content.replace("</p>", "</p> ")), flags=re.DOTALL)
            break

    if match == False:
        clean = re.sub('Recommended content:.*?:','', strip_tags(content.replace("</p>", "</p> ")), flags=re.DOTALL)

    return clean

def condensed_content(content):
    for key in special_chars:
        content = content.replace(key, special_chars[key])

    content = content.replace('\n \n','')
    content = content.replace('\n ','')
    content = re.sub(' +',' ', content)
    content = content.replace(' :', ':')

    for key in abbreviations:
        content = content.replace(key, abbreviations[key])
        content = content.replace(key.capitalize(), abbreviations[key])

    return content.strip()

def save_workout(slug, raw, condensed):
    workout = {}
    workouts = []
    print 'Slug: ', slug
    print 'Raw: ', raw
    print 'Condensed: ', condensed

    # split the workout for open and experiencd tracks
    for key in headers:
        if headers[key] is not None and headers[key] in condensed:
            workouts = condensed.split(headers[key])
            dict_key = headers[key].split(" ")[0].lower()
            other_dict_key = 'experienced' if dict_key == 'open' else 'open'

            workout[dict_key] = workouts[1].replace(headers[key] + "\n", "")
            workout[other_dict_key] = workouts[0].replace(key + " \n", "")
            break

        # not split workouts
        elif key in condensed:
            workout['open'] = condensed.replace(key, "")
            workout['experienced'] = condensed.replace(key, "")
            break

    # if split, set variables
    if len(workout) == 2:
        open_workout = workout['open']
        experienced_workout = workout['experienced']
    else:
        open_workout = condensed
        experienced_workout = condensed

    print 'Open: ', open_workout
    print 'Experienced: ', experienced_workout

    workout = Workout(slug=slug, raw=raw, open=open_workout, experienced=experienced_workout, sent=False, ACL=ACL({}))
    return workout.save()

if __name__ == '__main__':
    register(PARSE['APPLICATION_ID'], PARSE['REST_API_KEY'], master_key=PARSE['MASTER_KEY'])

    # Get most recent blog programming posts
    blog_posts = get_programming_urls()

    # For each blog post...
    for post in blog_posts:
        response = requests.get(post)
        text = response.text

        soup = bs4.BeautifulSoup(text.replace('<div class="col-right"></p>', '<div class="col-right">'))

        # Get content for each post
        content = str(soup.select('div.col-right')).strip('[]')

        if content == "":
            content = str(soup.select('div.single-post-content')).strip('[]')

        # If the post contains a WOD
        if has_wod(content):

            # Get slug from the URL
            slug = post.replace("http://www.bowerycrossfit.com/programming-", "").strip("/")

            # Does the slug already exist?
            slug_exist = Workout.Query.all().filter(slug=slug).limit(1)

            if slug_exist.count() == 0:
                # If not, save the workout
                raw = clean_content(content)
                condensed = condensed_content(raw)
                save_workout(slug, raw, condensed)
            else:
                print 'No new workouts.'



