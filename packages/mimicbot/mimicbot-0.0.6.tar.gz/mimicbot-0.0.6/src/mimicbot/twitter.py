import os

import twitter

class Client():

    twitter = None

    def __init__(self, name):
        # load Twitter app consumer details
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

    def post(self, text):
        self.twitter.statuses.update(status=text)
