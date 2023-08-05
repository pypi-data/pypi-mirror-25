.. image:: https://img.shields.io/pypi/status/timeutils.svg
    :target: https://gitlab.com/cmick/timeutils

.. image:: https://badge.fury.io/py/timeutils.svg
    :target: https://badge.fury.io/py/timeutils

.. image:: https://readthedocs.org/projects/timeutils/badge
   :target: http://timeutils.readthedocs.io

.. image:: https://img.shields.io/pypi/pyversions/timeutils.svg
   :target: https://pypi.python.org/pypi/timeutils

.. image:: https://img.shields.io/pypi/l/timeutils.svg
   :target: https://gitlab.com/cmick/timeutils/blob/master/LICENSE

timeutils
=========

timeutils is a Python package providing a set of methods and classes to
accurately measure elapsed time.

Documentation
-------------

The documentation is hosted on http://timeutils.readthedocs.io/en/0.2.2/

Installation
------------

Latest from the `source <https://gitlab.com/cmick/timeutils>`_::

    git clone https://gitlab.com/cmick/timeutils.git
    cd timeutils
    python setup.py install

Using `PyPI <https://pypi.python.org/pypi/timeutils>`_::

    pip install timeutils

Examples
--------

.. code :: pycon

    >>> from timeutils import Stopwatch
    >>> sw = Stopwatch(start=True)
    >>> sw.elapsed_seconds
    16.282313108444214
    >>> str(sw.stop())
    '0:01:30.416023'
    >>> sw.elapsed.human_str()
    '1 min, 30 secs'
