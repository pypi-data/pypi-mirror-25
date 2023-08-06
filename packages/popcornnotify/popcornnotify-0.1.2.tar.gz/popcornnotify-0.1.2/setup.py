from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='popcornnotify',
    version='0.1.2',
    description='Send simple emails and text messages from one API',
    long_description=long_description,
    url='https://popcornnotify.com',
    author='Abe',
    author_email='abe@popcornnotify.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: Communications :: Email',
        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=['popcornnotify', ],
    install_requires=['requests'],
)
