from distutils.core import setup
setup(
  name = 'bamboo-cli',
  packages = ['bamboo-cli'], # this must be the same as the name above
  version = '0.1',
  description = 'A cli tool to report to pandibamboo',
  author = 'Christoffer Oleander Nielsen',
  author_email = 'christoffer.o.nielsen@gmail.com',
  url = 'https://github.com/coleander/bamboo-cli',
  download_url = 'https://github.com/coleander/bamboo-cli/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['cli', 'bamboo', 'pandiweb'], # arbitrary keywords
  classifiers = ['Development Status :: 3 - Alpha'],
)
