import re

from pyparsing import nestedExpr, QuotedString

class Filter:

    def check_not_empty(self, text):
        if not text:
            raise Exception("empty string")

    def check_too_long(self, text):
        if len(text) > 140:
            raise Exception("too long")

    def check_contains_link(self, text):
        # update tests for only using ":"
        if re.findall("http(s?):", text):
            raise Exception("contains link")

    def check_contains_username(self, text):
        if re.findall("@\w+", text):
            raise Exception("contains username")

    def check_syntax(self, text):
        # delete contractions
        text = re.sub("\w('|’)\w", "", text)
        # valid syntax
        paired_exprs = \
            nestedExpr('(',')') | \
            nestedExpr('[',']') | \
            nestedExpr('{','}') | \
            QuotedString("\"") | \
            QuotedString("'") | \
            QuotedString("“", endQuoteChar="”") | \
            QuotedString("‘", endQuoteChar="’") | \
            QuotedString("*") \
        # strip out matched syntax
        stripped_line = paired_exprs.suppress().transformString(text)
        # if there are any quotes or parentheses left, they were not
        # properly nested
        if any(unwanted in stripped_line for unwanted in "()[]{}\"'“”‘’*"):
            raise Exception("bad syntax")

    def run(self, text):
        self.check_not_empty(text)
        self.check_too_long(text)
        self.check_contains_link(text)
        self.check_contains_username(text)
        self.check_syntax(text)

# import language_check

# tool = language_check.LanguageTool('en-GB')

# print(text)
# matches = tool.check(text)
# text = language_check.correct(text, matches)
