from distutils.core import setup

setup(
  name = 'bc_first_pypi_pkg',
  packages = ['bc_first_pypi_pkg'], # this must be the same as the name above
  version = '0.1.1',
  description = 'A test lib',
  author = 'Pao zhi',
  author_email = 'phillpchen@hotmail.com',
  url = 'https://github.com/bc/test', # use the URL to the github repo
  download_url = 'https://github.com/bc/test/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
)
