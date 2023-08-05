from os.path import join, dirname
from setuptools import setup

setup(
  name = 'sinknal',
  packages = ['sinknal'],
  version = '0.1a0',
  description = 'Rsync caller coordinator',
  long_description = open(join(dirname(__file__), 'README.txt')).read(),
  install_requires=[],
  author = 'Gamaliel Espinoza M.',
  author_email = 'gamaliel.espinoza@gmail.com',
  url = 'https://github.com/gamikun/sinknal',
  keywords = ['rsync', 'coordinator', 'daemon'],
  classifiers = [],
)
