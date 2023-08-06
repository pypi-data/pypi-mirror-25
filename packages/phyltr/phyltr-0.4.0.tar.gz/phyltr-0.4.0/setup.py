#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='phyltr',
    version='0.4.0',
    description='Unix filters for manipulating and analysing (samples of) phylogenetic trees represented in the Newick format',
    author='Luke Maurits',
    author_email='luke@maurits.id.au',
    url='https://github.com/lmaurits/phyltr',
    license="GPL3",
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    packages = ['phyltr','phyltr/commands', 'phyltr/plumbing', 'phyltr/utils'],
    entry_points = {
        'console_scripts': ['phyltr=phyltr.main:run_command'],
    },
    requires=['ete3'],
    install_requires=['ete3']

)
