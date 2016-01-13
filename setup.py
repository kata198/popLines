#!/usr/bin/env python

import sys

from setuptools import setup

if __name__ == '__main__':

    summary = 'Tools to pop lines from the head/tail of a file to stdout. Makes files into queues!'
    try:
        with open('README.rst', 'rt') as f:
            long_description = f.read()
    except Exception as e:
        sys.stderr.write('Error reading description: %s\n' %(str(e),))
        long_description = summary

    setup(name='popLines',
        version='1.0',
        scripts=['popHead', 'popTail', 'popRandom'],
        modules=['PopLines'],
        packages=['PopLines'],
        provides=['PopLines'],
        keywords=['popLines', 'file', 'head', 'tail', 'random', 'queue', 'pop', 'lines', 'text', 'popHead', 'popTail', 'popRandom' ],
        url='https://github.com/kata198/popLines',
        long_description=long_description,
        author='Tim Savannah',
        author_email='kata198@gmail.com',
        maintainer='Tim Savannah',
        maintainer_email='kata198@gmail.com',
        license='GPLv2',
        description=summary,
        classifiers=['Development Status :: 5 - Production/Stable',
            'Programming Language :: Python',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Database',
            'Topic :: Text Processing',
            'Topic :: Utilities',
        ]
        
    )

#vim: set ts=4 sw=4 expandtab

