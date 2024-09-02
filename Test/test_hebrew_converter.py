import unittest
import hebrew_converter

class TestTimes(unittest.TestCase):
    def test_convert_to_words(self):
        ...

    def test_calc_month_name(self):
        self.assertEqual(hebrew_converter.calc_month_name(5784, 1), "Nissan")

    def test_is_leap_year(self):
        self.assertTrue(hebrew_converter.is_leap_year(5784))
        self.assertFalse(hebrew_converter.is_leap_year(5785))
        self.assertFalse(hebrew_converter.is_leap_year(5786))
        self.assertTrue(hebrew_converter.is_leap_year(5787))
        self.assertFalse(hebrew_converter.is_leap_year(5788))
        self.assertFalse(hebrew_converter.is_leap_year(5789))
        self.assertTrue(hebrew_converter.is_leap_year(5790))
        self.assertFalse(hebrew_converter.is_leap_year(5791))
        self.assertFalse(hebrew_converter.is_leap_year(5792))
        self.assertTrue(hebrew_converter.is_leap_year(5793))
        self.assertFalse(hebrew_converter.is_leap_year(5794))
        self.assertTrue(hebrew_converter.is_leap_year(5795))
        self.assertFalse(hebrew_converter.is_leap_year(5796))
        self.assertFalse(hebrew_converter.is_leap_year(5797))
        self.assertTrue(hebrew_converter.is_leap_year(5798))
        self.assertFalse(hebrew_converter.is_leap_year(5799))
        self.assertFalse(hebrew_converter.is_leap_year(5800))
        self.assertTrue(hebrew_converter.is_leap_year(5801))
        self.assertFalse(hebrew_converter.is_leap_year(5802))
