"""TimeSpan"""
# Author: Michal Ciesielczyk
# Licence: MIT
import datetime


class TimeSpan(datetime.timedelta):
    """Stores a time span.

    :param seconds: precise number of seconds in the time span.
    :type seconds: float
    """

    def __new__(cls, seconds=0, microseconds=0, milliseconds=0,
                minutes=0, hours=0, days=0, weeks=0):
        return datetime.timedelta.__new__(cls, days=days, seconds=seconds,
                                          microseconds=microseconds,
                                          milliseconds=milliseconds,
                                          minutes=minutes, hours=hours,
                                          weeks=weeks)

    def total_hours(self):
        return (self.days * 24 + self.seconds / 3600 +
                self.microseconds / 3600000000)

    def total_minutes(self):
        return (self.days * 1440 + self.seconds / 60 +
                self.microseconds / 60000000)

    def total_milliseconds(self):
        return (self.days * 86400000 + self.seconds * 1000 +
                self.microseconds / 1000)

    def human_str(self, trim_zeros=True):
        """Returns a human-readable :py:class:`~.timespan.TimeSpan` object,
        represented as time units such as days, hours, minutes, and seconds.
        """
        if self.total_seconds() < 1:
            return "{:d} ms".format(self.microseconds // 1000)
        human = []
        if self.days > 0 or not trim_zeros:
            human.append("{:d} days".format(self.days))
        units = [("hours", 3600), ("mins", 60), ("secs", 1)]
        seconds_left = self.seconds
        for name, secs in units:
            if trim_zeros and self.seconds < secs:
                continue
            value = seconds_left // secs
            seconds_left %= secs
            if value == 1:
                name = name.rstrip('s')
            human.append("{:d} {:s}".format(value, name))
        return ', '.join(human)
