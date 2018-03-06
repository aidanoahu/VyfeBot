import praw
import sched
import time
import tweepy

# Credentials removed from Reddit & Twitter OAuth.
# I plan to make the program fetch them from a file in the future that you can customize.

class PeriodicScheduler(object):
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def setup(self, interval, action, actionargs=()):
        action(*actionargs)
        self.scheduler.enter(interval, 1, self.setup, (interval, action, actionargs))

    def run(self):
        self.scheduler.run()


recent_tweet = ''


def periodic_event():
    try:
        reddit = praw.Reddit(client_id='-',
                             client_secret='-', password='-',
                             user_agent='VyfeBot', username='VyfeBot')

        subreddit = reddit.subreddit('VyfeLinks')

        new_vyfelink = subreddit.new(limit=1)

        consumer_key = '-'
        consumer_secret = '-'
        access_token = '-'
        access_token_secret = '-'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        global recent_tweet

        for submission in new_vyfelink:
            if not recent_tweet is submission.title:
                tweet = submission.title
                api.update_status(status=(tweet + '\n\n' + submission.shortlink))
                recent_tweet = submission.title
    except tweepy.TweepError as e:
        print(e.reason)


INTERVAL = 10
periodic_scheduler = PeriodicScheduler()
periodic_scheduler.setup(INTERVAL, periodic_event)
periodic_scheduler.run()
