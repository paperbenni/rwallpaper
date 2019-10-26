import cv2
import time
from urllib.parse import urlparse
import wget
import os
import praw
from urllib import request

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


subreddit = reddit.subreddit('wallpapers')

submissions = subreddit.top(time_filter='week', limit=100)

wallpaperurl = False

primarylist = []

for i in submissions:
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
        if ending == '.png':
            print('png image')
            checkpicture = 'wallpaper.png'
            request.urlretrieve(url, './wallpaper.png')
        height, width, _ = cv2.imread(checkpicture).shape
        ratio = width / height
        if ratio <= 1.8 and ratio >= 1.7:
            print('found wallpaper')
            if os.path.exists('wallpaper.bak'):
                os.remove('wallpaper.bak')
            return True
    return False


if not getwallpaper(primarylist):
    getwallpaper(submissions)

os.system('feh --bg-scale ~/paperbenni/' + checkpicture)
