import os
import sys
import random
import time
import shutil

import click

import mimicbot
from mimicbot import twitter

@click.group()
def cli():
    pass

@cli.command()
@click.argument("bot_name")
def create(bot_name):
    "Create a bot."
    home = os.path.expanduser("~")
    bot_dir = os.path.join(home, ".mimicbot", bot_name)
    if not os.path.isdir(bot_dir):
        click.secho("Creating bot...", fg="green")
        os.makedirs(bot_dir)
        click.secho("Done!", fg="green")
    else:
        click.secho("Bot exists!", fg="red")

@cli.command()
def list():
    "List bots."
    home = os.path.expanduser("~")
    bots_dir = os.path.join(home, ".mimicbot")
    for filename in os.listdir(bots_dir):
        if os.path.isdir(os.path.join(bots_dir, filename)):
            click.echo(filename)

@cli.command()
@click.argument("bot_name")
def delete(bot_name):
    "Delete a bot."
    home = os.path.expanduser("~")
    bot_dir = os.path.join(home, ".mimicbot", bot_name)
    if os.path.isdir(bot_dir):
        click.secho("Deleting bot...", fg="green")
        shutil.rmtree(bot_dir)
        click.secho("Done!", fg="green")
    else:
        click.secho("Not a bot!", fg="red")

@cli.command()
@click.argument("bot_name")
def auth(bot_name):
    "Authenticate a bot against Twitter."
    # TODO: before doing this, wipe the existing auth file to force re-auth
    client = twitter.Client(bot_name)
    click.echo("auth")

@cli.command()
@click.argument("bot_name")
def reset():
    "Reset a bot's training."
    click.echo("reset")

@cli.command()
@click.option("--latest-tweets", metavar="USERNAME",
    help="Train from a user's latest tweets.")
@click.option("--csv-archive", metavar="FILENAME",
    help="Train from Twitter CSV tweet archive.")
@click.argument("bot_name")
def train(bot_name, latest_tweets, csv_archive):
    "Train a bot from source material."
    bot = mimicbot.Bot(bot_name)
    if latest_tweets:
        client = twitter.Client(bot_name)
        tweets = client.get_latest_tweets(latest_tweets)
        bot.generator.train_latest_tweets(tweets)
    if csv_archive:
        bot.generator.train_csv(csv_archive)
    # TODO error out if both are missing
    # TODO add option for just reading lines from a file. for when someone is
    # running a bot based off of someone else's account. given that our "latest
    # tweets" only grabs the last 200 each time

@cli.command()
# TODO make username a config ini setting
# TODO add help docs saying that "not authorized" can be thrown if the training
# TODO account is locked
@click.option("--train", metavar="USERNAME",
    help="Train the bot from recent tweets before running.")
@click.option("--use-context", is_flag=True,
    help="Set context from LENGTH recent tweets.")
@click.option("--manual-context",
    help="Set context as TEXT.")
@click.option("--random-exit", default=0,
    help="Randomly exit instead of running. 1/INTEGER chance of succeeding.")
@click.option("--random-delay", metavar="SECONDS",
    help="Run with a random delay.")
@click.option("--dry-run", is_flag=True,
    help="Dry run. Do not post.")
@click.argument("bot_name")
def run(bot_name, train, use_context, manual_context, random_exit, random_delay, dry_run):
    "Run a bot."
    if random_exit:
        roll = random.randint(1, random_exit)
        if roll != 1:
            click.secho("Randomly exiting!", fg="green")
            return
    if random_delay:
        seconds = random.randint(1, int(random_delay))
        click.secho("Sleeping for %ss..." % seconds, fg="green")
        time.sleep(seconds)
    bot = mimicbot.Bot(bot_name)
    if train:
        # TODO: remove duplication from command above
        client = twitter.Client(bot_name)
        tweets = client.get_latest_tweets(train)
        bot.generator.train_latest_tweets(tweets)
    click.secho("Getting text...", fg="green")
    # TODO move the twitter client stuff into the bot
    text = bot.get_text(use_context, manual_context)
    click.secho("Got text...", fg="green")
    click.echo("%s" % text)
    if dry_run:
        click.secho("Dry run. Exiting...", fg="green")
    else:
        click.secho("Posting...", fg="green")
        client = twitter.Client(bot_name)
        client.post(text)
