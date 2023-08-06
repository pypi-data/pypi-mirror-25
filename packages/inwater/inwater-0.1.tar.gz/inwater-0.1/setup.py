from distutils.core import setup

setup(
  name = 'inwater',
  packages = ['inwater'], # this must be the same as the name above
  version = '0.1',
  description = 'A random test lib',
  author = 'Raul Bardaji',
  author_email = 'rbardaji@gmail.com',
  url = 'https://github.com/rbardaji/inwater', # use the URL to the github repo
  download_url = 'https://github.com/rbardaji/inwater/archive/0.1.tar.gz',
  keywords = ['emso', 'obsea', 'emodnet', 'ocean'], # arbitrary keywords
  classifiers = ['Development Status :: 3 - Alpha', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Natural Language :: English', 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering'],
)