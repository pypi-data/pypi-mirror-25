.. image:: https://readthedocs.org/projects/timeutils/badge/?version=latest
   :target: http://timeutils.readthedocs.io/en/latest/?badge=latest

timeutils
=========

timeutils is a Python package providing a set of methods and classes to
accurately measure elapsed time.

Documentation
-------------

The documentation is hosted on http://timeutils.readthedocs.io/en/latest/

Installation
------------

Latest from the `source <https://gitlab.com/cmick/timeutils>`_::

    git clone https://gitlab.com/cmick/timeutils.git
    cd timeutils
    python setup.py install

Examples
--------

.. code :: pycon

    >>> from timeutils import Stopwatch
    >>> sw = Stopwatch(start=True)
    >>> sw.elapsed_seconds
    16.282313108444214
    >>> str(sw.stop())
    '00:01:30.416'
    >>> sw.elapsed.human_str()
    '1 min, 30 secs'
