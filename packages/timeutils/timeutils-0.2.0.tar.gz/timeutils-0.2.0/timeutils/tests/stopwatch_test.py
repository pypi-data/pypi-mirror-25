# Author: Michal Ciesielczyk
# Licence: MIT
import unittest
from time import sleep
from random import random

from ..stopwatch import Stopwatch


def _rand_time():
    return 0.3 + (random() - 0.5) / 10


class StopwatchTest(unittest.TestCase):
    def start_test(self):
        t = _rand_time()
        sw = Stopwatch()
        sw.start()
        sleep(t)
        elapsed = sw.elapsed_seconds
        self.assertTrue(elapsed > 0)

        sleep(t)
        self.assertTrue(sw.elapsed_seconds > elapsed)

    def stop_test(self):
        t = _rand_time()
        sw = Stopwatch()
        sw.start()
        sleep(t)
        sw.stop()
        elapsed = sw.elapsed_seconds
        sleep(t)
        self.assertEqual(sw.elapsed_seconds, elapsed)

    def start_stop_test(self):
        t = _rand_time()
        sw = Stopwatch()
        sw.start()
        sleep(t)
        sw.stop()
        self.assertAlmostEqual(sw.elapsed_seconds, t, 2)

    def is_running_test(self):
        sw = Stopwatch()
        self.assertFalse(sw.is_running)
        sw.start()
        self.assertTrue(sw.is_running)
        sw.stop()
        self.assertFalse(sw.is_running)

    def autostart_test(self):
        t = _rand_time()
        sw = Stopwatch(start=True)
        sleep(t)
        sw.stop()
        self.assertAlmostEqual(sw.elapsed_seconds, t, 2)

    def suspend_test(self):
        t = _rand_time()
        sw = Stopwatch()
        sw.start()
        sw.suspend()
        elapsed = sw.elapsed_seconds
        sleep(t)
        self.assertEqual(sw.elapsed_seconds, elapsed)

    def resume_test(self):
        t = _rand_time()
        sw = Stopwatch()
        sw.start()
        sw.suspend()
        elapsed = sw.elapsed_seconds
        sw.resume()
        sleep(t)
        self.assertTrue(sw.elapsed_seconds > elapsed)

        sw = Stopwatch()
        sw.start()
        sleep(t)
        sw.suspend()
        sleep(t)
        sw.resume()
        sleep(t)
        sw.stop()
        self.assertAlmostEqual(sw.elapsed_seconds, 2 * t, 2)

    def is_suspended_test(self):
        t = _rand_time()
        sw = Stopwatch()
        sw.start()
        sleep(t)
        sw.suspend()
        self.assertTrue(sw.is_suspended)

    def reset_test(self):
        t = _rand_time()
        sw = Stopwatch()
        sw.start()
        sleep(t)
        elapsed = sw.elapsed
        sw.reset()
        self.assertNotEqual(sw.elapsed_seconds, elapsed)
        self.assertTrue(sw.elapsed_seconds == 0)

if __name__ == '__main__':
    unittest.main()
