#!/usr/bin/env python

from setuptools import setup

_locals = {}
with open('pepper/_version.py') as fp:
    exec(fp.read(), None, _locals)
version = _locals['__version__']

setup(name='ff_pepper',
      version=version,
      description='Gluon node provision utility',
      author='Freifunk Darmstadt',
      author_email='info@darmstadt.freifunk.net',
      url='https://git.darmstadt.ccc.de/ffda/pepper',
      packages=['pepper', 'pepper.frontend'],
      classifiers=[
          'Topic :: Utilities',
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      install_requires=['paramiko', 'requests', 'pyyaml', 'beautifulsoup4'],
      scripts=['bin/pepper', 'bin/pepper-ssh']
      )
