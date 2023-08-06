from distutils.core import setup
setup(
  name = 'leolabs',
  packages = ['leolabs'],
  version = '0.1.6',
  description = 'LeoLabs Api',
  author = 'LeoLabs, Inc.',
  author_email = 'support@leolabs.space',
  url = 'https://github.com/leolabs-space/leo-api-python',
  keywords = ['leolabs', 'radar', 'space', 'leo', 'orbit', 'propagation', 'norad'],
  classifiers = [],
  install_requires = ['requests'],
  entry_points = {
    'console_scripts': [
      'leolabs=leolabs.bin.cli:main'
    ]
  }
)
