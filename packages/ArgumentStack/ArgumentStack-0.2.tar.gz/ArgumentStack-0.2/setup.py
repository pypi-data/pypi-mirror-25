from distutils.core import setup
setup(
  name = 'ArgumentStack',
  packages = ['ArgumentStack'], # this must be the same as the name above
  version = '0.2',
  description = 'An easy way to create command-line application with nicely organized arguments.',
  author = 'Stefan Nožinić',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/ArgumentStack', # use the URL to the github repo
  download_url = 'https://github.com/fantastic001/ArgumentStack/tarball/0.1', 
  keywords = ['parsing', 'arguments', 'cli'], 
  package_dir = {'ArgumentStack': 'src'},
  classifiers = [],
  install_requires=[] # dependencies listed here 
)
