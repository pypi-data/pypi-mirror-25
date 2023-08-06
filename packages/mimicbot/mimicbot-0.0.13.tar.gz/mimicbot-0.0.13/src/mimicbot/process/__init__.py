import re
import random

class Processor:

    def correct_case(self, text):
        # lower case
        text = text.lower()
        # upper case exception
        text = re.sub("(^|[^\w])i([^\w]|$)", r"\1I\2", text)
        return text

    def trim_spaces(self, text):
        # chop leading spaces
        text = re.sub("^ +", "", text)
        # chop trailing spaces
        text = re.sub(" +$", "", text)
        return text

    def trim_trailing_full_stop(self, text):
        # drop trailing full stops
        # but not if there's more than one full stop
        text = re.sub("([^.])\.$", r"\1", text)
        return text

    def replace_curly_quotes(self, text):
        text = re.sub("“", "\"", text)
        text = re.sub("”", "\"", text)
        text = re.sub("‘", "'", text)
        text = re.sub("’", "'", text)
        return text

    def expand_elipsis(self, text):
        text = re.sub("…", "...", text)
        return text

    def strip_usernames(self, text):
        # don't mention people
        text = re.sub("@\w+", "@irlnomi", text)
        return text

    def run(self, text):
        # text = self.correct_case(text)
        text = self.trim_spaces(text)
        text = self.trim_trailing_full_stop(text)
        text = self.replace_curly_quotes(text)
        text = self.expand_elipsis(text)
        text = self.strip_usernames(text)
        return text
