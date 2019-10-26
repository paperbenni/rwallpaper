#!/usr/bin/env python3

#########################################################
## fetch and set top 1080p wallpaper from r/wallpapers ##
#########################################################

from urllib import request
import cv2
import time
from urllib.parse import urlparse
import wget
import os
import praw
import random
import subprocess
import re

monitors = int(subprocess.Popen
               ('xrandr | egrep "[^s]connected" | wc -l',
                shell=True, stdout=subprocess.PIPE).communicate()[0])


print('wallpaper changer started')

checkpicture = ''

os.chdir(os.environ['HOME'] + '/paperbenni')
if os.path.exists('wallpaper.png'):
    os.rename('wallpaper.png', 'wallpaper.bak')
elif os.path.exists('wallpaper.jpg'):
    os.rename('wallpaper.jpg', 'wallpaper.bak')


# import environment variables into python
def getenv(var, default):
    if var in os.environ:
        return os.environ[var]
    else:
        return default


clientid = getenv('CLIENTID', 'U3OVuCLPbRY64A')
clientsecret = getenv('CLIENTSECRET', 'b9dPOM1KO9PlhjTgYcOOyGAt6qQ')

reddit = praw.Reddit(client_id=clientid,
                     client_secret=clientsecret,
                     user_agent='rwallpapers')

# choose between multiple subreddits
redditlist = ['wallpaper', 'wallpapers']

if monitors == 2:
    redditlist.append('multiwall')

reddittopic = random.choice(redditlist)
subreddit = reddit.subreddit(reddittopic)

submissions = subreddit.top(time_filter='week', limit=100)

wallpaperurl = False

primarylist = []

for i in submissions:
    if reddittopic == 'multiwall':
        if '3840' in i.title and \
                '1080' in i.title:
            primarylist.append(i)
            print('1080p picture found')
    else:
        if '1920' in i.title and \
                '1080' in i.title:
            primarylist.append(i)
            print('1080p picture found')


def getwallpaper(sublist):
    print('processing wallpapers')
    global checkpicture
    if len(list(sublist)) == 0:
        print('no posts to process')
        return False
    for submission in sublist:
        if submission.over_18:
            print('skipped nsfw')
            continue
        url = str(submission.url)
        print(submission.title, url)
        ending = os.path.splitext(url)[1]
        if not ending in ['.jpg', '.png']:
            print('skipping submission')
            continue
        if ending == '.jpg':
            print('jpg image')
            checkpicture = 'wallpaper.jpg'
            request.urlretrieve(url, './wallpaper.jpg')
        elif ending == '.png':
            print('png image')
            checkpicture = 'wallpaper.png'
            request.urlretrieve(url, './wallpaper.png')
        elif re.compile('https://imgur.com/a/.*').match(url):
            scriptpath = os.path.dirname(os.path.realpath(__file__))
            os.system('bash ' + scriptpath + '/imgur.sh ' + url)
            checkpicture = 'wallpaper.png'
            
        height, width, _ = cv2.imread(checkpicture).shape
        ratio = width / height
        if not reddittopic == 'multiwall':
            if ratio <= 1.8 and ratio >= 1.7:
                print('found wallpaper')
                if os.path.exists('wallpaper.bak'):
                    os.remove('wallpaper.bak')
                return True
        else:
            if ratio <= 3.5 and ratio >= 3.6:
                print('found dual monitor wallpaper')
                if os.path.exists('wallpaper.bak'):
                    os.remove('wallpaper.bak')
                return True
    return False


if not getwallpaper(primarylist):
    getwallpaper(submissions)

if reddittopic == 'multiwall':
    os.system('feh --bg-scale --no-xinerama ~/paperbenni' + checkpicture)

os.system('feh --bg-scale ~/paperbenni/' + checkpicture)
