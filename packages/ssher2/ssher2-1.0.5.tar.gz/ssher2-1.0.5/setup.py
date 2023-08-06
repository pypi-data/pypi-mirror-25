import codecs
import os
import sys
  
try:
    from setuptools import setup
except:
    from distutils.core import setup
  
def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
  
  
  
NAME = "ssher2"
  
PACKAGES = ["ssher",]
  
DESCRIPTION = "ssh sftp..."
  
LONG_DESCRIPTION = read("README.txt")
  
KEYWORDS = "ssh python python3"
  
AUTHOR = "Andrew liu"
  
AUTHOR_EMAIL = "1185978974@qq.com"
  
URL = "https://pypi.python.org/pypi/ssher2"
  
VERSION = "1.0.5"
  
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
    install_requires = ['paramiko'],
    include_package_data=True,
    zip_safe=True,
)
  
