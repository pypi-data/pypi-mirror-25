from setuptools import setup
setup(
  name = 'dgcli_master',
  packages = ['dgcli_master'],
  version = '0.0.001',
  description = 'Command Line Interface for Deep Generator',
  author = 'Deep Generator Inc',
  author_email = 'contact@deepgenerator.com',
  keywords = ['deepgenerator', 'cli', 'deep learning', 'infrastructure'],
  classifiers = [],
  entry_points = {
    'console_scripts': ['dgcli_master=dgcli_master.dgcli_master:main'],
  },
)
