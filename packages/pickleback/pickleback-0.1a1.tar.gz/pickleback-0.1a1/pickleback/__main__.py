from __future__ import print_function
import sys
import runpy

from pickleback import register


def main():
    if len(sys.argv) == 1:
        print('Usage: {prog} /path/to/python-script.py [script-args...]\n'
              'Usage: {prog} -m path.to.module [script-args...]\n'
              '\n'
              'Loads matplotlib backend for pkl extension before running'
              'script')
        sys.exit(1)

    register()
    del sys.argv[0]
    if sys.argv[0] == '-m':
        del sys.argv[0]
        runpy.run_module(sys.argv[0], run_name='__main__')
    else:
        runpy.run_path(sys.argv[0], run_name='__main__')


if __name__ == '__main__':
    main()
