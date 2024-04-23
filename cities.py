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
        return self.data[city][0], self.data[city][1]

    def get_city_timezone(self, latitude, longitude):
        return timezone(self.tf.timezone_at(lng=longitude, lat=latitude))


class CapeTown:
    latitude = -33.9249
    longitude = 18.4241


class Johannesburg:
    latitude = -26.2041
    longitude = 28.0473
