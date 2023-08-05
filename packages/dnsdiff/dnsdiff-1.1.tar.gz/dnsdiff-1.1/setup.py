from distutils.core import setup
setup(
  name = 'dnsdiff',
  packages = ['dnsdiff'], # this must be the same as the name above
  scripts=['dnsdiff/dnsdiff'],
  version = '1.1',
  description = 'Utility to quickly suss out discrepancies between nameservers',
  author = 'M Anzuoni',
  author_email = 'me.anzuoni@gmail.com',
  url = 'https://github.com/gawkermedia/dnsdiff', # use the URL to the github repo
  download_url = 'https://github.com/gawkermedia/dnsdiff/archive/1.1.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'dns',], # arbitrary keywords
  classifiers = [],
  install_requires=['dnspython']

)