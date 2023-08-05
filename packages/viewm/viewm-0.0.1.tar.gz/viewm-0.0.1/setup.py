#!/usr/bin/env python

from setuptools import setup

import os


def version():
    setupDir = os.path.dirname(os.path.realpath(__file__))
    versionFile = open(os.path.join(setupDir, 'viewm', 'VERSION'))
    return versionFile.readline().strip()

if __name__ == '__main__':

    dirName = os.path.dirname(__file__)
    if dirName and os.getcwd() != dirName:
        os.chdir(dirName)

    setup(
        name='viewm',
        version=version(),
        author='Donovan Parks',
        author_email='donovan.parks@gmail.com',
        maintainer='Donovan Parks',
        maintainer_email='donovan.parks@gmail.com',
        packages=['viewm'],
        scripts=['bin/viewm'],
        package_data={'viewm' : ['VERSION','./data/*.tsv']},
        url='http://pypi.python.org/pypi/viewm/',
        license='GPLv3',
        description='Visualization of functional modules to aid biological interpretation of genomes.',
        classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          ],
        install_requires=["svgwrite>=1.1.9"],
    )
