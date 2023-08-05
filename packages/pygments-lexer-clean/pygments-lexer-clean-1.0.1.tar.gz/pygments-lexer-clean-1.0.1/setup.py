"""The setuptools based setup module for pygments-lexer-clean."""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pygments-lexer-clean',
    version='1.0.1',
    description='A Pygments lexer for the Clean language',
    long_description=long_description,
    url='https://github.com/clean-cloogle/pygments-lexer-clean',
    author='Camil Staps',
    author_email='info@camilstaps.nl',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities',
    ],
    keywords='syntax highlighting clean pygments',
    py_modules=['pygments_clean']
)
