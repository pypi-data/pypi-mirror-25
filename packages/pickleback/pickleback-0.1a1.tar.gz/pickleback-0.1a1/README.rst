Matplotlib pickle backend : pickleback
======================================

Matplotlib backend defining export to pickle (extension `.pkl` or `.pickle`).

|version| |licence| |py-versions|

|issues| |build| |docs| |coverage|


Interactive usage::

    >>> import pickleback
    >>> pickleback.register()
    >>> my_figure.savefig('/path/to/output.pkl')  # doctest: +SKIP

Script-based usage, assuming my script uses ``savefig`` to the path specified
by ``-o``::

    $ python -m pickleback /path/to/myscript.py -o /path/to/output.pkl

or::

    $ python -m pickleback -m my_module.command -o /path/to/output.pkl



.. |py-versions| image:: https://img.shields.io/pypi/pyversions/pickleback.svg
    :alt: Python versions supported

.. |version| image:: https://badge.fury.io/py/pickleback.svg
    :alt: Latest version on PyPi
    :target: https://badge.fury.io/py/pickleback

.. |build| image:: https://travis-ci.org/jnothman/pickleback.svg?branch=master
    :alt: Travis CI build status
    :scale: 100%
    :target: https://travis-ci.org/jnothman/pickleback

.. |issues| image:: https://img.shields.io/github/issues/jnothman/pickleback.svg
    :alt: Issue tracker
    :target: https://github.com/jnothman/pickleback

.. |coverage| image:: https://coveralls.io/repos/github/jnothman/pickleback/badge.svg
    :alt: Test coverage
    :target: https://coveralls.io/github/jnothman/pickleback

.. |docs| image:: https://readthedocs.org/projects/pickleback/badge/?version=latest
     :alt: Documentation Status
     :scale: 100%
     :target: https://pickleback.readthedocs.io/en/latest/?badge=latest

.. |licence| image:: https://img.shields.io/badge/Licence-BSD-blue.svg
     :target: https://opensource.org/licenses/BSD-3-Clause
