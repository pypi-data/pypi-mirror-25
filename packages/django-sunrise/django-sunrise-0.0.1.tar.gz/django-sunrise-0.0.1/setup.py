import os
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
  name = 'django-sunrise',
  packages=find_packages(),
  include_package_data=True,
  version = '0.0.1',
  description = 'An enterprise application development framework',
  author = 'Partha.Konda',
  author_email = 'parthasaradhi1992@gmail.com',
  url = '', 
  download_url = '', 
  keywords = ['django-sunrise', 'sunrise'], 
  classifiers = [],
  install_requires=[
        "django"
    ],
  zip_safe=True)
