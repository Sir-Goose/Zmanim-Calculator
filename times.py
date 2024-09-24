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

    def __init__(self, city: str, date_offset: int, current_date: date | None=None) -> None:
        self.city = city
        self.offset = date_offset
        self.latitude, self.longitude = self.cities.get_coordinates(city)
        self.location = LocationInfo(longitude=self.longitude, latitude=self.latitude)
        if current_date is None:
            self.current_date = datetime.now(timezone('UTC')).date()
        else:
            self.current_date = current_date
        self.current_date = self.current_date + timedelta(days=date_offset)
        time_zone_name = self.tf.timezone_at(lng=self.longitude, lat=self.latitude)
        if time_zone_name:
            self.str_timezone = time_zone_name
        else:
            self.str_timezone = "UTC"
        self.object_timezone = timezone(self.str_timezone)

    def dawn(self) -> str:
        sun_times = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=16.9)
        dawn = sun_times['dawn']
        dawn = dawn.astimezone(self.object_timezone)
        dawn = self.format_time(dawn)
        return dawn

    def earliest_tallit_tefillin(self) -> str:
        sun_times = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=10.2)
        tallit_tefillin = sun_times['dawn']
        tallit_tefillin = tallit_tefillin.astimezone(self.object_timezone)
        tallit_tefillin = self.format_time(tallit_tefillin)
        return tallit_tefillin

    def sunrise(self) -> str:
        sun_times = sun(self.location.observer, date=self.current_date)
        sunrise = sun_times['sunrise']
        sunrise = sunrise.astimezone(self.object_timezone)
        sunrise = self.format_time(sunrise)
        return sunrise

    def latest_shema(self) -> str:
        minutes = int(self.shaah_zmanit() * 60 * 3)
        latest_shema = self.hanetz_amiti() + timedelta(minutes=minutes)
        latest_shema = self.format_time(latest_shema)
        return latest_shema

    def latest_shacharit(self) -> str:
        minutes = int(self.shaah_zmanit() * 60 * 4)
        latest_shacharit = self.hanetz_amiti() + timedelta(minutes=minutes)
        latest_shacharit = self.format_time(latest_shacharit)
        return latest_shacharit

    def hanetz_amiti(self) -> datetime:
        sun_times = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)
        true_sunrise = sun_times['dawn']
        true_sunrise = true_sunrise.astimezone(self.object_timezone)
        return true_sunrise

    def shkiah_amitis(self) -> datetime:
        sun_times = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)
        true_sunset = sun_times['dusk']
        true_sunset = true_sunset.astimezone(self.object_timezone)
        return true_sunset

    def midday(self) -> str:
        start_time = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dawn']
        end_time = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dusk']

        time_diff = end_time - start_time
        midday = start_time + time_diff / 2

        midday = midday.astimezone(self.object_timezone)
        midday = self.format_time(midday)
        return midday

    def earliest_mincha(self) -> str:
        minutes = int(self.shaah_zmanit() * 60 * 6.5)
        earliest_mincha = self.hanetz_amiti() + timedelta(minutes=minutes)
        earliest_mincha = self.format_time(earliest_mincha)
        return earliest_mincha

    def mincha_ketana(self) -> str:
        minutes = int(self.shaah_zmanit() * 60 * 2.5)
        mincha_ketana = self.shkiah_amitis() - timedelta(minutes=minutes)
        mincha_ketana = self.format_time(mincha_ketana)
        return mincha_ketana

    def plag_hamincha(self) -> str:
        minutes = int(self.shaah_zmanit() * 60 * 1.25)
        plag_hamincha = self.shkiah_amitis() - timedelta(minutes=minutes)
        plag_hamincha = self.format_time(plag_hamincha)
        return plag_hamincha

    def sunset(self) -> str:
        sun_times = sun(self.location.observer, date=self.current_date)
        sunset = sun_times['sunset']
        sunset = sunset.astimezone(self.object_timezone)
        sunset = self.format_time(sunset)
        return sunset

    def nightfall(self) -> str:
        sun_times = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=8.5)

        nightfall = sun_times['dusk']
        nightfall = nightfall.astimezone(self.object_timezone)
        nightfall_time = self.format_time(nightfall)
        return nightfall_time

    def midnight(self) -> str:
        tomorrow_date = self.current_date + timedelta(days=1)
        start_time = sun(self.location.observer, date=self.current_date, dawn_dusk_depression=1.583)['dusk']
        end_time = sun(self.location.observer, date=tomorrow_date, dawn_dusk_depression=1.583)['dawn']

        time_diff = end_time - start_time

        midpoint = start_time + time_diff / 2
        midpoint = midpoint.astimezone(self.object_timezone)
        midnight = self.format_time(midpoint)
        return midnight

    def shaah_zmanit(self) -> float:
        true_sunrise = self.hanetz_amiti()
        true_sunset = self.shkiah_amitis()

        time_diff = true_sunset - true_sunrise
        prop_hour = time_diff.seconds / 3600 / 12

        return prop_hour

    def get_current_hebrew_date(self) -> str:
        hebrew_date = hebrew.from_gregorian(self.current_date.year, self.current_date.month, self.current_date.day)
        hebrew_date = str(hebrew_date)
        hebrew_date = hebrew_date.replace('(', ' ').replace(')', ' ').replace(',', '')
        return hebrew_date

    def get_current_hebrew_date_words(self) -> str:
        number_date = self.get_current_hebrew_date()
        number_date = number_date.strip()
        number_date = number_date.split(' ')
        #print(number_date)
        word_date = hebrew_converter.convert_to_words(number_date[0], number_date[1], number_date[2])
        return word_date

    def get_hebrew_date_30_days_ago(self) -> str:
        thirty_days_ago = self.current_date - timedelta(days=30)
        hebrew_date = hebrew.from_gregorian(thirty_days_ago.year, thirty_days_ago.month, thirty_days_ago.day)
        hebrew_date = str(hebrew_date)
        hebrew_date = hebrew_date.replace('(', ' ').replace(')', ' ').replace(',', '')
        return hebrew_date

    def get_current_english_date(self) -> str:
        english_date = str(self.current_date)
        english_date = english_date.replace('-', ' ')
        return english_date

    def get_current_english_date_words(self) -> str:
        english_date = self.current_date.strftime("%d %B %Y")
        return english_date

    def is_friday(self) -> bool:
        day = sun(self.location.observer, date=self.current_date)['sunrise']
        day = day.strftime("%A")
        if day == "Friday":
            return True
        else:
            return False

    def is_saturday(self) -> bool:
        day = sun(self.location.observer, date=self.current_date)['sunrise']
        day = day.strftime("%A")
        if day == "Saturday":
            return True
        else:
            return False

    def candle_lighting(self) -> str:
        sunset = self.sunset()
        sunset = datetime.strptime(sunset, "%H:%M")
        sunset = sunset - timedelta(minutes=18)
        candle_lighting = sunset.strftime("%H:%M")
        return candle_lighting

    def format_time(self, time) -> str:
        if time.second >= 30:
            time += timedelta(minutes=1)
        time = time.strftime("%H:%M")
        return time
