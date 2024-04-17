from flask import Flask, render_template, request
import csv
import times
import cities

app = Flask(__name__)
Times = times.Times()


def read_cities_from_csv(file_path):
    cities_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            cities_list.append(row)
    return cities_list


def strip_cords(cities_list):
    out_list = []
    for city in cities_list:
        out_list.append(city[0])
    return out_list


@app.route('/', methods=['GET'])
def home():
    cities_list = read_cities_from_csv('cities.csv')
    cities_list = strip_cords(cities_list)
    return render_template('home.html', cities=cities_list)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    query = query.replace('+', ' ')
    return index(query)





def index(selected_city="Cape Town"):
    # selected_city = request.args.get('selectedCity')
    if selected_city:
        city = selected_city
        print("selected City: ", city)
        # Call the relevant functions based on the selected city
        dawn = Times.dawn(city)
        earliest_tallit = Times.earliest_tallit_tefillin(city)
        sunrise = Times.sunrise(city)
        latest_shema = Times.latest_shema(city)
        latest_shacharit = Times.latest_shacharit(city)
        midday = Times.midday(city)
        earliest_mincha = Times.earliest_mincha(city)
        mincha_ketana = Times.mincha_ketana(city)
        plag_hamincha = Times.plag_hamincha(city)
        sunset = Times.sunset(city)
        nightfall = Times.nightfall(city)
        midnight = Times.midnight(city)
        shaah_zmanit = round(Times.shaah_zmanit(city) * 60, 2)
        current_date = Times.get_current_hebrew_date(city)
    else:
        # Cape Town is the default city
        dawn = Times.dawn("Cape Town")
        earliest_tallit = Times.earliest_tallit_tefillin("Cape Town")
        sunrise = Times.sunrise("Cape Town")
        latest_shema = Times.latest_shema("Cape Town")
        latest_shacharit = Times.latest_shacharit("Cape Town")
        midday = Times.midday("Cape Town")
        earliest_mincha = Times.earliest_mincha("Cape Town")
        mincha_ketana = Times.mincha_ketana("Cape Town")
        plag_hamincha = Times.plag_hamincha("Cape Town")
        sunset = Times.sunset("Cape Town")
        nightfall = Times.nightfall("Cape Town")
        midnight = Times.midnight("Cape Town")
        shaah_zmanit = round(Times.shaah_zmanit("Cape Town") * 60, 2)
        city = "Cape Town"
        current_date = Times.get_current_hebrew_date("Cape Town")

    cities_list = read_cities_from_csv('cities.csv')

    return render_template('times.html', current_date=current_date, dawn=dawn, earliest_tallit=earliest_tallit,
                           sunrise=sunrise, latest_shema=latest_shema, latest_shacharit=latest_shacharit,
                           midday=midday, earliest_mincha=earliest_mincha, mincha_ketana=mincha_ketana,
                           plag_hamincha=plag_hamincha, sunset=sunset, nightfall=nightfall, midnight=midnight,
                           shaah_zmanit=shaah_zmanit, city=city, cities=cities_list)


if __name__ == '__main__':
    app.run()
