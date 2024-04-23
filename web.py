from flask import Flask, render_template, request, session, redirect, url_for
import csv
import times
import cities
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
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
    date_offset = int(request.args.get('date_offset', 0))
    session['date_offset'] = date_offset
    return index(query, date_offset)


@app.route('/update_offset', methods=['POST'])
def update_offset():
    city = request.form.get('city')
    action = request.form.get('action')
    current_offset = int(request.form.get('current_offset'))

    if action == 'increment':
        new_offset = current_offset + 1
    else:
        new_offset = current_offset - 1

    return redirect(url_for('search', query=city, date_offset=new_offset))


def index(selected_city="Cape Town", date_offset=0):
    # selected_city = request.args.get('selectedCity')
    if selected_city:
        city = selected_city
        print("selected City: ", city)
        # Call the relevant functions based on the selected city
        dawn = Times.dawn(city, date_offset)
        earliest_tallit = Times.earliest_tallit_tefillin(city, date_offset)
        sunrise = Times.sunrise(city, date_offset)
        latest_shema = Times.latest_shema(city, date_offset)
        latest_shacharit = Times.latest_shacharit(city, date_offset)
        midday = Times.midday(city, date_offset)
        earliest_mincha = Times.earliest_mincha(city, date_offset)
        mincha_ketana = Times.mincha_ketana(city, date_offset)
        plag_hamincha = Times.plag_hamincha(city, date_offset)
        sunset = Times.sunset(city, date_offset)
        nightfall = Times.nightfall(city, date_offset)
        midnight = Times.midnight(city, date_offset)
        shaah_zmanit = round(Times.shaah_zmanit(city, date_offset) * 60, 2)
        current_date_hebrew = Times.get_current_hebrew_date_words(city, date_offset)
        current_date_english = Times.get_current_english_date_words(city, date_offset)
        is_friday = Times.is_friday(city, date_offset)
        candle_lighting = Times.candle_lighting(city, date_offset)
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
        current_date_hebrew = Times.get_current_hebrew_date_words("Cape Town")
        current_date_english = Times.get_current_english_date_words("Cape Town")
        is_friday = Times.is_friday("Cape Town")
        candle_lighting = Times.candle_lighting("Cape Town")

    cities_list = read_cities_from_csv('cities.csv')

    return render_template('times.html', current_date_english=current_date_english,
                           current_date_hebrew=current_date_hebrew, dawn=dawn, earliest_tallit=earliest_tallit,
                           sunrise=sunrise, latest_shema=latest_shema, latest_shacharit=latest_shacharit,
                           midday=midday, earliest_mincha=earliest_mincha, mincha_ketana=mincha_ketana,
                           plag_hamincha=plag_hamincha, sunset=sunset, nightfall=nightfall, midnight=midnight,
                           shaah_zmanit=shaah_zmanit, city=city, cities=cities_list, is_friday=is_friday,
                           candle_lighting=candle_lighting)


if __name__ == '__main__':
    app.run()
