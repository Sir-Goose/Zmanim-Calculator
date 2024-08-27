import unittest
import times
from datetime import datetime, date
from pytz import timezone

class TestTimes(unittest.TestCase):
    CityTimes = times.Times("Cape Town", 0, date(2024, 8 , 23))
    def test_dawn(self):
        self.assertEqual(self.CityTimes.dawn(), "10:00")



if __name__ == '__main__':
    unittest.main()
