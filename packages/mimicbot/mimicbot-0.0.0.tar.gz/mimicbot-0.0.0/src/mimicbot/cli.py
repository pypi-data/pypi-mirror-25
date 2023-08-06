import sys
import random
import time

import mimicbot
from mimicbot import twitter

# syntax: mimicbot username chance post
def main(*args):
    name = sys.argv[1]
    chance = int(sys.argv[2])
    roll = random.randint(1, chance)
    if roll != 1:
        print("not this time: %s, %s" % (roll, chance))
        return
    bot = mimicbot.Bot(name)
    text = bot.get_text()
    print("finished\n")
    print(text)
    try:
        # basically, try to access this arg. if it doesn't exit. quit
        post = sys.argv[3]
        # sleep, so that if you have multiple bots in cron, and they happen to
        # fire on the same minute, we reduce the chance that they fire at
        # exactly the same time
        seconds = random.randint(1, 60)
        print("sleeping for %s seconds" % seconds)
        time.sleep(seconds)
        client = twitter.Client(name)
        client.post(text)
    except IndexError:
        pass

