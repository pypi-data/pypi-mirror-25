from distutils.core import setup


setup(
  name = 'rgbshift',
  packages = ['rgbshift'], # this must be the same as the name above
  version = '0.0.2',
  description = 'RGB shift CLI tool',
  author = 'cqsd',
  author_email = 'colloquiasd@gmail.com',
  url = 'https://github.com/cqsd/glitch-suite',
  download_url = 'https://github.com/cqsd/glitch-suite/archive/0.0.2.tar.gz',
  keywords = ['glitch'], # arbitrary keywords
  classifiers = [],
  scripts=['rgbshift/rgbshift'],
  install_requires=[
      'pillow',
  ],
)
