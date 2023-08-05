"""TimeSpan"""
# Author: Michal Ciesielczyk
# Licence: MIT


class TimeSpan:
    def __init__(self, t):
        self._time = t

    @property
    def days(self):
        return int(self._time // 86400)

    @property
    def hours(self):
        return int(self._time // 3600) % 24

    @property
    def total_hours(self):
        return int(self._time // 3600)

    @property
    def minutes(self):
        return int(self._time // 60) % 60

    @property
    def total_minutes(self):
        return int(self._time // 60)

    @property
    def seconds(self):
        return int(self._time) % 60

    @property
    def total_seconds(self):
        return int(self._time)

    @property
    def milliseconds(self):
        return int(self._time * 1000) % 1000

    @property
    def total_milliseconds(self):
        return int(self._time * 1000)

    def human_str(self, trim_zeros=True):
        """Returns a human-readable :py:class:`~.timespan.TimeSpan` object,
        represented as time units such as days, hours, minutes, and seconds.
        """
        if self._time < 1:
            return "{:d} ms".format(self.milliseconds)
        units = [("days", 86400), ("hours", 3600), ("mins", 60), ("secs", 1)]
        human = []
        seconds_left = self._time
        for name, secs in units:
            if trim_zeros and self._time < secs:
                continue
            value = int(seconds_left // secs)
            seconds_left %= secs
            if value == 1:
                name = name.rstrip('s')
            human.append("{:d} {:s}".format(value, name))
        return ', '.join(human)

    def __str__(self):
        if self.days == 0:
            return "{:02d}:{:02d}:{:02d}.{:03d}".format(
                self.hours, self.minutes, self.seconds, self.milliseconds)
        return "{}d {:2d}h {:2d}m".format(self.days, self.hours, self.minutes)
