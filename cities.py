import csv
from pytz import timezone
from timezonefinder import TimezoneFinder


class Cities:
    data = {}
    tf = TimezoneFinder()

    def cities(self):
        with open('cities.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                city = row[0]
                latitude = float(row[1])
                longitude = float(row[2])
                self.data[city] = (latitude, longitude)

            print("City data loaded.")

    def get_coordinates(self, city):
        latitude: float = self.data[city][0]
        longitude: float = self.data[city][1]
        assert latitude, longitude <= 180
        return latitude, longitude

    def get_city_timezone(self, latitude: float, longitude: float):
        assert latitude, longitude <= 180
        try:
            str_time: str | None = self.tf.timezone_at(lng=longitude, lat=latitude)
            if str_time is None:
                raise ValueError(
                    f"Unable to determine timezone for coordinates: lat={latitude}, lng={longitude}")
            date_time_time = timezone(str_time)
        except:
            date_time_time = timezone("UTC")
        return date_time_time


class CapeTown:
    latitude = -33.9249
    longitude = 18.4241


class Johannesburg:
    latitude = -26.2041
    longitude = 28.0473
