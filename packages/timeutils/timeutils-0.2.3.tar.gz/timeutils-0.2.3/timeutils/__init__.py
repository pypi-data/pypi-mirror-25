"""A set of methods and classes to accurately measure elapsed time.

See https://gitlab.com/cmick/timeutils for more information.

Examples
--------

    >>> from timeutils import Stopwatch
    >>> sw = Stopwatch(start=True)
    >>> sw.elapsed_seconds
    16.282313108444214
    >>> str(sw.stop())
    '00:01:30.416'
    >>> sw.elapsed.human_str()
    '1 min, 30 secs'

.. seealso::

    Documentation of the :py:class:`~.stopwatch.Stopwatch` class.
"""
from ._version import __version__

from .stopwatch import Stopwatch


def current_time_millis():
    """Returns the difference, measured in milliseconds, between the current
    time and midnight, January 1, 1970 UTC.
    """
    import time
    return int(round(time.time() * 1000))
