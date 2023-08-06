import os
import random
import re
import csv
import html

import dateutil
from dateutil import parser

from MarkovText import MarkovText

# TODO: don't use them like this
from whoosh import fields, index, qparser, analysis, sorting
import whoosh.query

import click

import pprint
pp = pprint.PrettyPrinter(indent=4, depth=9)

MIN_KEYWORD_NUMBER=1
MAX_KEYWORD_NUMBER=20

MIN_TWEETS_NUMBER=100
MAX_TWEETS_NUMBER=200

class MarkovGenerator:

    dir = None

    index = None

    chain = None

    context = None

    results = None

    def __init__(self, dir):
        self.dir = dir

    def get_index(self):
        stem_ana = analysis.StemmingAnalyzer()
        schema = fields.Schema(
            id=fields.ID(unique=True),
            datetime=fields.DATETIME(sortable=True),
            reply=fields.BOOLEAN,
            retweet=fields.BOOLEAN,
            text=fields.TEXT(analyzer=stem_ana, stored=True)
        )
        index_dir = os.path.join(self.dir, "index")
        if os.path.exists(index_dir):
            self.index = index.open_dir(index_dir)
        else:
            os.mkdir(index_dir)
            self.index = index.create_in(index_dir, schema)

    def search(self, query, number):
        self.get_index()

        import pprint
        pp = pprint.PrettyPrinter(indent=4, depth=9)

        with self.index.searcher() as searcher:
            # improve relevance! form query from keywords
            keywords = searcher.key_terms_from_text("text", query, numterms=number)
            keyword_query = " ".join(
                [keyword for keyword, score in keywords])

            # if we don't find any keywords. for example, we're not actually
            # looking up context tweets
            # TODO find better way of doing this
            if not keyword_query:
                keyword_query = "*"

            print("keyword query: %s" % keyword_query)

            parser = qparser.QueryParser(
                "text", self.index.schema, group=qparser.OrGroup)
            query = parser.parse(keyword_query)

            restrict_retweets = whoosh.query.Term("retweet", True)

            results = searcher.search(query, mask=restrict_retweets, limit=MAX_TWEETS_NUMBER)
            for result in results:
                yield result["text"]

    def get_context(self):
        if self.context:
            return self.context

        self.get_index()

        from whoosh.qparser.dateparse import DateParserPlugin

        datetimes = sorting.FieldFacet("datetime", reverse=True)
        parser = qparser.QueryParser("text", self.index.schema)
        query = parser.parse("*")
        searcher = self.index.searcher()

        restrict_replies = whoosh.query.Term("reply", True)

        results = searcher.search(
            query, mask=restrict_replies, sortedby=datetimes, limit=MAX_TWEETS_NUMBER)

        click.secho("Adding to context...", fg="green")

        context = set()

        for result in results:
            text = result["text"]

            click.secho(text)

            import re

            # don't want these influence context
            # drop usernames
            text = re.sub(r"@[^ ]+", " ", text)
            # drop links
            text = re.sub(r"http(s?)://[^ ]+", " ", text)
            # drop cut-off text from the end of manual rts
            text = re.sub(r"[^ ]+…$", " ", text)

            context.update(text.split(" "))

        # split and discard empty strings
        context = " ".join(filter(None, context))

        click.secho("Processed context:", fg="green")
        click.secho(context)

        self.context = context

        return self.context

    def read_csv(self, filename):
        with open(filename, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=",", quotechar="\"")
            for row in reader:
                if row[0] == "tweet_id":
                    # skip header row
                    continue
                id = row[0]
                datetime = dateutil.parser.parse(row[3])
                reply = True if row[1] else False
                retweet = True if row[6] else False
                text = html.unescape(row[5])
                # turn newlines into something a markov chain is aware of
                text = re.sub(r"\n", " %NEWLINE% ", text)
                yield id, datetime, reply, retweet, text

    def train_csv(self, filename):
        self.get_index()
        writer = self.index.writer()
        for id, datetime, reply, retweet, text in self.read_csv(filename):
            print("writing doc: %s, %s, %s, %s, %s" % (id, datetime, reply, retweet, text))
            writer.update_document(id=id, datetime=datetime, reply=reply, retweet=retweet, text=text)
        writer.commit()
        doc_count = self.index.doc_count()
        print("doc count: %s" % doc_count)

    def train_latest_tweets(self, tweets):
        # TODO: fix duplication with train_csv method
        self.get_index()
        writer = self.index.writer()
        for tweet in tweets:
            id = tweet["id_str"]
            datetime = dateutil.parser.parse(tweet["created_at"])
            reply = True if tweet["in_reply_to_status_id"] else False
            retweet = True if tweet["retweeted"] else False
            text = html.unescape(tweet["text"])
            # turn newlines into something a markov chain is aware of
            text = re.sub(r"\n", " %NEWLINE% ", text)
            print("writing doc: %s, %s, %s, %s, %s" % (id, datetime, reply, retweet, text))
            writer.update_document(id=id, datetime=datetime, reply=reply, retweet=retweet, text=text)
        writer.commit()
        doc_count = self.index.doc_count()
        print("doc count: %s" % doc_count)


    def get_diff_context(self, use_context, manual_context):
        context = ""
        if use_context:
            click.secho("Searching for context tweets...", fg="green")
            context = self.get_context()
        if manual_context:
            context = manual_context
        return context

    def get_results(self, use_context, manual_context, number=MIN_KEYWORD_NUMBER):

        context = self.get_diff_context(use_context, manual_context)
        click.secho("Getting tweets for markov chain using %s keywords..." % number, fg="green")
        results = list(self.search(context, number))

        results_count = len(results)

        # TODO make this config var
        if results_count >= MIN_TWEETS_NUMBER:
            click.secho("Got %s tweets!" % results_count, fg="green")
            self.results = results
            return
        else:
            click.secho("Only got %s tweets! Widening the net..." % results_count, fg="red")

            if number < MAX_KEYWORD_NUMBER:
                # increment number and recurse
                number +=1
                self.get_results(use_context, manual_context, number)
            else:
                click.secho("Hit max keyword number. Switching to contextless...", fg="red")
                self.get_results(False, "*")

    def run(self, use_context, manual_context):
        if not self.results:
            self.get_results(use_context, manual_context)
        self.chain = MarkovText.Markov()
        for result in self.results:
            self.chain.add_to_dict(result)
        sentence_count = random.randint(1, 6)
        output = self.chain.create_sentences(sentence_count)
        output = re.sub(r"\s?%NEWLINE%\s?", "\n", output)
        return output

