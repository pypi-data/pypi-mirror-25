# Author: Michal Ciesielczyk
# Licence: MIT
import unittest

from ..timespan import TimeSpan


class TimeSpanTest(unittest.TestCase):
    def test_human_str(self):
        ts = TimeSpan(0)
        self.assertEqual(ts.human_str(), "0 ms")

        ts = TimeSpan(0.55)
        self.assertEqual(ts.human_str(), "550 ms")

        ts = TimeSpan(1.5)
        self.assertEqual(ts.human_str(), "1 sec")

        ts = TimeSpan(100)
        self.assertEqual(ts.human_str(), "1 min, 40 secs")

        ts = TimeSpan(360)
        self.assertEqual(ts.human_str(), "6 mins, 0 secs")

        ts = TimeSpan(10000000)
        self.assertEqual(ts.human_str(), "115 days, 17 hours, 46 mins, 40 secs")

        ts = TimeSpan(250.5)
        self.assertEqual(ts.human_str(trim_zeros=False),
                         "0 days, 0 hours, 4 mins, 10 secs")

    def test_str(self):
        ts = TimeSpan(1000.4534)
        self.assertEqual(str(ts), "00:16:40.453")

        ts = TimeSpan(21000.4534)
        self.assertEqual(str(ts), "05:50:00.453")

        ts = TimeSpan(321000.4534)
        self.assertEqual(str(ts), "3d 17h 10m")

        ts = TimeSpan(263400.4534)
        self.assertEqual(str(ts), "3d  1h 10m")

        ts = TimeSpan(266500.4534)
        self.assertEqual(str(ts), "3d  2h  1m")


if __name__ == '__main__':
    unittest.main()
