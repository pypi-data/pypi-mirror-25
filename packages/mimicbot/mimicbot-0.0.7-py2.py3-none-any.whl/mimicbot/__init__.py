import os

from mimicbot import filter, generate, process

__version__ = "0.0.7"

class Bot:

    dir = None

    generator = None

    filter = None

    processor = None

    def __init__(self, name):
        home = os.path.expanduser("~")
        self.dir = os.path.join(home, ".mimicbot", name)
        if not os.path.isdir(self.dir):
            raise Exception("bot dir does not exist")
        self.generator = generate.Generator(self.dir)
        self.filter = filter.Filter()
        self.processor = process.Processor()

    def _handle(self, text):
        self.filter.run(text)
        # print("filter passed")
        return self.processor.run(text)

    def get_text(self, use_context, manual_context):
        text = None
        for i in range(100000):
            text = self.generator.run(use_context, manual_context)
            # print("\ngenerated: %s" % text)
            try:
                return self._handle(text)
            except Exception as error:
                print("error: %s" % error)
                continue
        raise Exception("too many failed attempts to filter text")

