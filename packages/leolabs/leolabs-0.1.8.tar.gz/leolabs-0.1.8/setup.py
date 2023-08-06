from distutils.core import setup
setup(
  name = 'leolabs',
  packages = ['leolabs'],
  version = '0.1.8',
  description = 'LeoLabs Api',
  author = 'LeoLabs, Inc.',
  author_email = 'support@leolabs.space',
  url = 'https://github.com/leolabs-space/leo-api-python',
  keywords = ['leolabs', 'radar', 'space', 'leo', 'orbit', 'propagation', 'norad'],
  classifiers = [],
  install_requires = ['requests'],
  entry_points = {
    'console_scripts': [
      'leolabs-cli=leolabs.bin.cli:main'
    ]
  }
)
