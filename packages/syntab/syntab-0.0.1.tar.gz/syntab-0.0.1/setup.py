import codecs
import os
import sys
  
try:
    from setuptools import setup
except:
    from distutils.core import setup
  
def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
  
  
  
NAME = "syntab"
  
PACKAGES = ["syntab",]
  
DESCRIPTION = "syn table schema from db1 to db2"
  
LONG_DESCRIPTION = read("README.txt")
  
KEYWORDS = "syn table python python3"
  
AUTHOR = "Andrew liu"
  
AUTHOR_EMAIL = "1185978974@qq.com"
  
URL = "https://pypi.python.org/pypi/syntab"
  
VERSION = "0.0.1"
  
LICENSE = "GPL"
  
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    install_requires = ['pymysql'],
    include_package_data=True,
    zip_safe=True,
)
  
