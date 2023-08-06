# from distutils.core import setup
from setuptools import setup
import os

def readfn(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='SimplePlayingCards',
    description='Simple pair of classes to represent playing cards in python games',
    long_description=readfn('README.md'),
    author='Chris Allison',
    url='https://github.com/ccdale/playingcards',
    download_url='https://github.com/ccdale/playingcards',
    author_email='chris.charles.allison+playingcards@gmail.com',
    version='1.0.39',
    license='MIT',
    py_modules=['playingcards'],
    scripts=[],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Topic :: Games/Entertainment',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.5',
      ],
)
