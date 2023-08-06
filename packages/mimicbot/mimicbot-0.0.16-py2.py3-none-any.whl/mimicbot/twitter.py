import os

import twitter

class Client():

    config = None

    username = None

    twitter = None

    def __init__(self, config, name):

        # this is bad. move it to the ini
        self.username = name

        self.config = config

        # load Twitter app consumer details
        # TODO: move this to ini file
        consumer_file = os.path.expanduser("~/.mimicbot/%s/consumer" % name)
        consumer_key, consumer_secret = twitter.read_token_file(consumer_file)

        # load authentication
        auth_file = os.path.expanduser("~/.mimicbot/%s/auth" % name)
        if not os.path.exists(auth_file):
            # none exist, so get authentication details
            twitter.oauth_dance(
                "mimicbot", consumer_key, consumer_secret, auth_file)

        # authenticate
        oauth_token, oauth_secret = twitter.read_token_file(auth_file)
        self.twitter = twitter.Twitter(auth=twitter.OAuth(
            oauth_token, oauth_secret, consumer_key, consumer_secret))

    def get_latest_tweets(self, username):
        tweets = self.twitter.statuses.user_timeline(
            screen_name=username, count=200)
        return tweets

    def post(self, text):

        import pprint
        pp = pprint.PrettyPrinter(indent=4, depth=9)

        odds = self.config.get(
            "behaviour", "reply_to_last_tweet_odds", fallback="0")

        import asteval
        from asteval import Interpreter
        aeval = Interpreter()

        odds = aeval(odds)
        pp.pprint(odds)

        import random

        if random.random() < odds:
            print("replying to last tweet")
            # randomly reply to last tweet
            tweets = self.twitter.statuses.user_timeline(
                screen_name=self.username, count=1)
            last_tweet_id = tweets[0]["id"]
            self.twitter.statuses.update(
                status=text, in_reply_to_status_id=last_tweet_id)
        else:
            print("not replying to last tweet")
            self.twitter.statuses.update(status=text)
