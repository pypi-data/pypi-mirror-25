from setuptools import setup

setup(
    name = "justpith",
    version = "0.0.34.36",
    author = "Antonio Carisita",
    author_email = "a.caristia@gmail.com",
    description = ("Core code for justpith infrastructure"),
    license = "GPL",
    keywords = "justpith's core",
    url = "http://packages.python.org/justpith",
    packages=['justpith','justpith.rabbit', 'justpith.mongo','justpith.mongo.teacher', 'justpith.mongo.factorizer', 'justpith.mongo.common', 'justpith.mongo.controller', 'justpith.mongo.web_app', 'justpith.logger', 'justpith.util'],
    install_requires=[
          'pika','pymongo','fluent-logger','nltk','stop-words'
    ],
    zip_safe=False
)
