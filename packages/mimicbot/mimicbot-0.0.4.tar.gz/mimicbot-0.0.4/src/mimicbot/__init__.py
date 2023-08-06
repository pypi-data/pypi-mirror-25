from mimicbot import filter, generate, process

__version__ = "0.0.4"

class Bot:

    generator = None

    filter = None

    processor = None

    def __init__(self, name):
        self.generator = generate.Generator(name)
        self.filter = filter.Filter()
        self.processor = process.Processor()

    def _handle(self, text):
        self.filter.run(text)
        # print("filter passed")
        return self.processor.run(text)

    def get_text(self):
        text = None
        for i in range(100000):
            text = self.generator.run()
            # print("\ngenerated: %s" % text)
            try:
                return self._handle(text)
            except Exception as error:
                print("error: %s" % error)
                continue
        raise Exception("too many failed attempts to filter text")

