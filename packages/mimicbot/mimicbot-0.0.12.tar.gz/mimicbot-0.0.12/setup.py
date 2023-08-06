import os
import imp

import setuptools

PACKAGE = "mimicbot"
DESCRIPTION = "A Twitter mimic bot"

pwd = os.path.join(os.path.dirname(__file__))
filename= os.path.join(pwd, "src", PACKAGE, "__init__.py")
version = imp.load_source(PACKAGE, filename).__version__

setuptools.setup(
    name=PACKAGE,
    version=version,
    description=DESCRIPTION,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software"
    ],
    author="Naomi Slater",
    author_email="nslater@tumbolia.org",
    url="https://github.com/nslater/mimicbot",
    keywords="twitter bot",
    license="Apache License 2.0",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    entry_points = {
        "console_scripts": ["mimicbot=mimicbot.cli:cli"],
    },
    test_suite="nose2.collector.collector",
    install_requires=[
      "setuptools",
      "markovify",
      "twitter",
      "pyparsing",
      "click",
      "Whoosh",
      "python-dateutil",
    ]
)
