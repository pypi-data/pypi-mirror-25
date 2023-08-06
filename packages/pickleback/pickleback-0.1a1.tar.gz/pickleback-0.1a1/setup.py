#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages


def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    try:
        # See setup.cfg
        setup(name='pickleback',
              version='0.1a1',
              packages=find_packages(),
              setup_requires=['pytest-runner'],
              tests_require=['pytest>=2.7', 'pytest-cov~=2.4', 'matplotlib'],
              )
        # We have considered installing a console script, but avoid it to
        # avoid environment mismatches that would break pickles.
    finally:
        del sys.path[0]
        os.chdir(old_path)
    return


if __name__ == '__main__':
    setup_package()
