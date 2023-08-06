from setuptools import setup
setup(
  name = 'lapps',
  packages = ['lapps'], # this must be the same as the name above
  version = '0.0.2',
  description = 'Python API for the Language Applications Grid',
  author = 'Keith Suderman',
  author_email = 'suderman@cs.vassar.edu',
  url = 'https://github.com/lappsgrid-incubator/python-api', # use the URL to the github repo
  download_url = 'https://github.com/lappsgrid-incubator/python-api/archive/0.0.2.tar.gz', # I'll explain this in a second
  keywords = ['lapps', 'lappsgrid', 'nlp', 'web services'], # arbitrary keywords
  install_requires = ['requests', 'zeep'],
  classifiers = [],
)