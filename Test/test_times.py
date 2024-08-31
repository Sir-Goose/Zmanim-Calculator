import unittest
import times
from datetime import datetime, date
from pytz import timezone

class TestTimes(unittest.TestCase):
    CityTimes = times.Times("Cape Town", 0, date(2024, 8 , 23))
    def test_dawn(self):
        self.assertEqual(self.CityTimes.dawn(), "05:57")
    def test_earliest_tallit_tefillin(self):
        self.assertEqual(self.CityTimes.earliest_tallit_tefillin(), "06:29")
    def test_sunrise(self):
        self.assertEqual(self.CityTimes.sunrise(), "07:15")
    def test_latest_shema(self):
        self.assertEqual(self.CityTimes.latest_shema(), "09:59")
    def test_latest_shacharit(self):
        self.assertEqual(self.CityTimes.latest_shacharit(), "10:55")
    def test_hanetz_amiti(self):
        # self.assertEqual(self.CityTimes.hanetz_amiti(), )
        ...
    def test_shkia_amitis(self):
        # self.assertEqual(self.CityTimes.shkiah_amitis(), )
        ...
    def test_midday(self):
        self.assertEqual(self.CityTimes.midday(), "12:49")
    def test_plag_hamincha(self):
        self.assertEqual(self.CityTimes.plag_hamincha(), "17:17")
    def test_sunset(self):
        self.assertEqual(self.CityTimes.sunset(), "18:22")
    def test_nightfall(self):
        self.assertEqual(self.CityTimes.nightfall(), "19:00")
    def test_midnight(self):
        self.assertEqual(self.CityTimes.midnight(), "00:48")
    def test_shaah_zmanit(self):
        self.assertEqual(round(self.CityTimes.shaah_zmanit() * 60, 2), 56.42)
    def test_get_current_hebrew_date(self):
        ...
    def test_get_current_hebrew_date_words(self):
        self.assertEqual(self.CityTimes.get_current_hebrew_date_words(), "19 Av 5784")
    def test_get_hebrew_date_30_days_ago(self):
        ...
    def test_get_current_english_date(self):
        ...
    def test_get_current_english_date_words(self):
        self.assertEqual(self.CityTimes.get_current_english_date_words(), "23 August 2024")
    def test_is_friday(self):
        self.assertEqual(self.CityTimes.is_friday(), True)
    def test_candle_lighting(self):
        self.assertEqual(self.CityTimes.candle_lighting(), "18:04")



if __name__ == '__main__':
    unittest.main()
