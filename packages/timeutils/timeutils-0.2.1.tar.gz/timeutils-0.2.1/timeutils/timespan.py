"""TimeSpan"""
# Author: Michal Ciesielczyk
# Licence: MIT


class TimeSpan:
    """Stores a time span with millisecond precision.

    :param seconds: precise number of seconds in the time span.
    :type seconds: float
    """

    def __init__(self, seconds):
        try:
            float(seconds)
        except:
            raise TypeError("seconds argument must be a number.")
        if seconds < 0.0:
            raise ValueError("seconds argument must be non-negative.")
        self._time = int(round(seconds, 3) * 1000)

    @property
    def days(self):
        return self._time // 86400000

    @property
    def hours(self):
        return self.total_hours % 24

    @property
    def total_hours(self):
        return self._time // 3600000

    @property
    def minutes(self):
        return self.total_minutes % 60

    @property
    def total_minutes(self):
        return self._time // 60000

    @property
    def seconds(self):
        return self.total_seconds % 60

    @property
    def total_seconds(self):
        return self._time // 1000

    @property
    def milliseconds(self):
        return self._time % 1000

    @property
    def total_milliseconds(self):
        return self._time

    def __eq__(self, other):
        if other is None or not isinstance(other, TimeSpan):
            return False
        return self.total_milliseconds == other.total_milliseconds

    def human_str(self, trim_zeros=True):
        """Returns a human-readable :py:class:`~.timespan.TimeSpan` object,
        represented as time units such as days, hours, minutes, and seconds.
        """
        if self._time < 1000:
            return "{:d} ms".format(self.milliseconds)
        units = [("days", 86400000), ("hours", 3600000),
                 ("mins", 60000), ("secs", 1000)]
        human = []
        millis_left = self._time
        for name, millis in units:
            if trim_zeros and self._time < millis:
                continue
            value = millis_left // millis
            millis_left %= millis
            if value == 1:
                name = name.rstrip('s')
            human.append("{:d} {:s}".format(value, name))
        return ', '.join(human)

    def __str__(self):
        if self.days == 0:
            return "{:02d}:{:02d}:{:02d}.{:03d}".format(
                self.hours, self.minutes, self.seconds, self.milliseconds)
        return "{}d {:2d}h {:2d}m".format(self.days, self.hours, self.minutes)
