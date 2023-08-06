import sys
from setuptools import setup

args = ' '.join(sys.argv).strip()
if not any(args.endswith(suffix) for suffix in ['setup.py check -r -s', 'setup.py sdist']):
    raise ImportError('parked',)

setup(
    author='Matt Bullock',
    author_email='matt.s.b.42@gmail.com',
    classifiers=['Development Status :: 7 - Inactive'],
    description='parked',
    license='Apache License 2.0',
    long_description='\nThis package is parked by Matt Bullock to protect against typo misdirection.\nSee https://github.com/mattsb42/pypi-parker for more information.\nDid you mean to install "pypi-parker"?',
    name='pypiparker',
    url='https://github.com/mattsb42/pypi-parker',
    version='0.0.9'
)
