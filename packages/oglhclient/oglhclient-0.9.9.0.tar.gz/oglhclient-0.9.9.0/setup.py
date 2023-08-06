import io
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'oglhclient',
  version = '0.9.9.0',
  description = 'An API client library for Opengear Lighthouse',
  long_description=long_description,
  author = 'Lighthouse Team',
  author_email = 'engineering@opengear.com',
  url = 'https://github.com/opengear/oglhclient',
  download_url = 'https://github.com/opengear/oglhclient/archive/v1.0p0.tar.gz',
  keywords = ['api', 'opengear', 'lighthouse'],
  classifiers = ['Programming Language :: Python :: 3', 'Programming Language :: Python :: 2'],
  install_requires = ['requests','pyyaml','future'],
  packages=find_packages(),
  package_data={'': ['*.raml', '*.html']},
)
