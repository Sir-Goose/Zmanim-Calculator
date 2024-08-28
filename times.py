from convertdate.gregorian import date
from pytz.tzinfo import DstTzInfo, StaticTzInfo
import requests
import cities
from typing import Any
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta
from pytz import timezone
from timezonefinder import TimezoneFinder
from convertdate import hebrew

import hebrew_converter

class Times:
    cities = cities.Cities()
    cities.cities()
    tf = TimezoneFinder()
    city: str
    offset: int
    current_date: date
    latitude: float
    longitude: float
    location: LocationInfo
    str_timezone: str
    object_timezone: StaticTzInfo | DstTzInfo | Any

    def __init__(self, city: str, date_offset: int, current_date: date | None=None):
        self.city = city
        self.offset = date_offset
        self.common_values(city, date_offset, current_date)

    def common_values(self, city, offset=0, current_date=None):
        # this needs a lot of checking
        self.latitude, self.longitude = self.cities.get_coordinates(city)
        self.location = LocationInfo(longitude=self.longitude, latitude=self.latitude)
        if current_date is None:
            self.current_date = datetime.now(timezone('UTC')).date()
        else:
            self.current_date = current_date
        self.current_date = self.current_date + timedelta(days=offset)
        time_zone_name = self.tf.timezone_at(lng=self.longitude, lat=self.latitude)
        if time_zone_name:
            self.str_timezone = time_zone_name
        else:
            self.str_timezone = "UTC"
        self.object_timezone = timezone(self.str_timezone)

    def dawn(self):
        dawn = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=16.9)
        dawn_time_utc = dawn['dawn']
        dawn_time_city = dawn_time_utc.astimezone(self.object_timezone)
        dawn_time = dawn_time_city.strftime("%H:%M")
        return dawn_time

    def earliest_tallit_tefillin(self):
        tallit_tefillin = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=10.2)
        tallit_tefillin_utc = tallit_tefillin['dawn']

        adjust_tallit_tefillin = tallit_tefillin_utc.astimezone(self.object_timezone)

        tallit_tefillin_time = adjust_tallit_tefillin.strftime("%H:%M")
        return tallit_tefillin_time

    def sunrise(self) -> str:
        sun_times = sun(self.location.observer, date=self.current_date)
        sunrise_utc = sun_times['sunrise']

        adjusted_sunrise = sunrise_utc.astimezone(self.object_timezone)

        sunrise_time = adjusted_sunrise.strftime("%H:%M")
        return sunrise_time

    def latest_shema(self):
        hanetz_amiti = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dawn']
        hanetz_amiti = hanetz_amiti.astimezone(self.object_timezone)
        hanetz_amiti = hanetz_amiti.strftime("%H:%M")

        time_obj = datetime.strptime(hanetz_amiti, "%H:%M")

        minutes = int(self.shaah_zmanit() * 60 * 3)

        latest_shema = time_obj + timedelta(minutes=minutes)
        latest_shema = latest_shema.strftime("%H:%M")

        return latest_shema

    def latest_shacharit(self):
        hanetz_amiti = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dawn']
        hanetz_amiti = hanetz_amiti.astimezone(self.object_timezone)
        hanetz_amiti = hanetz_amiti.strftime("%H:%M")

        time_obj = datetime.strptime(hanetz_amiti, "%H:%M")
        minutes = int(self.shaah_zmanit() * 60 * 4)
        latest_shacharit = time_obj + timedelta(minutes=minutes)

        latest_shacharit = latest_shacharit.strftime("%H:%M")

        return latest_shacharit

    def hanetz_amiti(self):
        dawn = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)

        dawn_time_utc = dawn['dawn']
        adjusted_time = timezone(self.str_timezone)
        adjusted_dawn_time = dawn_time_utc.astimezone(adjusted_time)

        hanetz_amiti_time = adjusted_dawn_time.strftime("%H:%M")
        return hanetz_amiti_time

    def shkiah_amitis(self):
        dusk = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)

        dusk_time_utc = dusk['dusk']

        dawn_time_utc_plus_2 = dusk_time_utc.astimezone(self.object_timezone)

        shkiah_amitis_time = dawn_time_utc_plus_2.strftime("%H:%M")
        return shkiah_amitis_time

    def midday(self):
        start_time = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dawn']
        end_time = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dusk']

        time_diff = end_time - start_time

        midpoint_time_utc = start_time + time_diff / 2

        midpoint_time_utc_plus_2 = midpoint_time_utc.astimezone(self.object_timezone)

        midday_time = midpoint_time_utc_plus_2.strftime("%H:%M")
        return midday_time

    def earliest_mincha(self):
        hanetz_amiti = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dawn']
        hanetz_amiti = hanetz_amiti.astimezone(self.object_timezone)
        hanetz_amiti = hanetz_amiti.strftime("%H:%M")

        time_obj = datetime.strptime(hanetz_amiti, "%H:%M")

        minutes = int(self.shaah_zmanit() * 60 * 6.5)

        earliest_mincha = time_obj + timedelta(minutes=minutes)

        earliest_mincha = earliest_mincha.strftime("%H:%M")

        return earliest_mincha

    def mincha_ketana(self):
        shkiah_amitis = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dusk']
        shkiah_amitis = shkiah_amitis.astimezone(self.object_timezone)
        shkiah_amitis = shkiah_amitis.strftime("%H:%M")

        time_obj = datetime.strptime(shkiah_amitis, "%H:%M")

        minutes = int(self.shaah_zmanit() * 60 * 2.5)

        mincha_ketana_time = time_obj - timedelta(minutes=minutes)

        mincha_ketana_time = mincha_ketana_time.strftime("%H:%M")

        return mincha_ketana_time

    def plag_hamincha(self):
        shkiah_amitis = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dusk']
        shkiah_amitis = shkiah_amitis.astimezone(self.object_timezone)
        shkiah_amitis = shkiah_amitis.strftime("%H:%M")

        time_obj = datetime.strptime(shkiah_amitis, "%H:%M")

        minutes = int(self.shaah_zmanit() * 60 * 1.25)

        plag_hamincha_time = time_obj - timedelta(minutes=minutes)

        plag_hamincha_time = plag_hamincha_time.strftime("%H:%M")

        return plag_hamincha_time

    def sunset(self):
        sun_times = sun(self.location.observer, date=self.current_date)

        sunset_utc = sun_times['sunset']

        sunset_utc_plus_2 = sunset_utc.astimezone(self.object_timezone)

        sunset_time = sunset_utc_plus_2.strftime("%H:%M")
        return sunset_time

    def nightfall(self):
        nightfall = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=6)

        nightfall_time_utc = nightfall['dusk']

        nightfall_time_utc_plus_2 = nightfall_time_utc.astimezone(self.object_timezone)

        nightfall_time = nightfall_time_utc_plus_2.strftime("%H:%M")
        return nightfall_time

    def midnight(self):
        tomorrow_date = self.current_date + timedelta(days=1)
        start_time = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dusk']
        end_time = sun(self.location.observer, date=tomorrow_date, dawn_dusk_depression=1.583)['dawn']

        time_diff = end_time - start_time

        midpoint_time_utc = start_time + time_diff / 2

        midpoint_time_utc_plus_2 = midpoint_time_utc.astimezone(self.object_timezone)

        midnight_time = midpoint_time_utc_plus_2.strftime("%H:%M")
        return midnight_time

    def shaah_zmanit(self):

        time1 = self.hanetz_amiti()
        time2 = self.shkiah_amitis()

        time1_obj = datetime.strptime(time1, "%H:%M")
        time2_obj = datetime.strptime(time2, "%H:%M")

        time_diff = time2_obj - time1_obj

        total_seconds = time_diff.total_seconds()

        hours = total_seconds / 3600

        result = hours / 12
        result = round(result, 4)

        return result

    def get_current_hebrew_date(self):
        hebrew_date = hebrew.from_gregorian(self.current_date.year, self.current_date.month, self.current_date.day)
        hebrew_date = str(hebrew_date)
        hebrew_date = hebrew_date.replace('(', ' ').replace(')', ' ').replace(',', '')
        return hebrew_date

    def get_current_hebrew_date_words(self):
        number_date = self.get_current_hebrew_date()
        number_date = number_date.strip()
        number_date = number_date.split(' ')
        print(number_date)
        word_date = hebrew_converter.convert_to_words(number_date[0], number_date[1], number_date[2])
        return word_date

    def get_hebrew_date_30_days_ago(self):
        thirty_days_ago = self.current_date - timedelta(days=30)
        hebrew_date = hebrew.from_gregorian(thirty_days_ago.year, thirty_days_ago.month, thirty_days_ago.day)
        hebrew_date = str(hebrew_date)
        hebrew_date = hebrew_date.replace('(', ' ').replace(')', ' ').replace(',', '')
        return hebrew_date

    def get_current_english_date(self):
        english_date = str(self.current_date)
        english_date = english_date.replace('-', ' ')
        return english_date

    def get_current_english_date_words(self):
        english_date = self.current_date.strftime("%d %B %Y")
        return english_date

    def is_friday(self):
        day = sun(self.location.observer, date=self.current_date)['sunrise']
        day = day.strftime("%A")
        if day == "Friday":
            return True
        else:
            return False

    def candle_lighting(self):
        sunset_time = self.sunset()
        sunset_time_obj = datetime.strptime(sunset_time, "%H:%M")
        sunset_time_obj = sunset_time_obj - timedelta(minutes=18)
        candle_lighting_time = sunset_time_obj.strftime("%H:%M")
        return candle_lighting_time
