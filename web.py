from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime, date
import csv
import times
import cities
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
#Times = times.Times()


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
    try:
        query = request.args.get('query')
        if query:
            query = query.replace('+', ' ')
            date_offset = int(request.args.get('date_offset', 0))
            session['date_offset'] = date_offset
            return index(query, date_offset)
    except:
        return index()
    return index()


@app.route('/update_offset', methods=['POST'])
def update_offset():
    city = request.form.get('city')
    action = request.form.get('action')
    offset = request.form.get('current_offset')
    new_offset = 0
    if offset:
        current_offset = int(offset)

        if action == 'increment':
            new_offset = current_offset + 1
        else:
            new_offset = current_offset - 1

    return redirect(url_for('search', query=city, date_offset=new_offset))


def get_times_data(city: str, date_offset: int):
    CityTimes = times.Times(city, date_offset)
    times_data = {}
    times_data['dawn'] = CityTimes.dawn()
    times_data['earliest_tallit'] = CityTimes.earliest_tallit_tefillin()
    times_data['sunrise'] = CityTimes.sunrise()
    times_data['latest_shema'] = CityTimes.latest_shema()
    times_data['latest_shacharit'] = CityTimes.latest_shacharit()
    times_data['midday'] = CityTimes.midday()
    times_data['earliest_mincha'] = CityTimes.earliest_mincha()
    times_data['mincha_ketana'] = CityTimes.mincha_ketana()
    times_data['plag_hamincha'] = CityTimes.plag_hamincha()
    times_data['sunset'] = CityTimes.sunset()
    times_data['nightfall'] = CityTimes.nightfall()
    times_data['midnight'] = CityTimes.midnight()
    times_data['shaah_zmanit'] = round(CityTimes.shaah_zmanit() * 60, 2)
    times_data['current_date_hebrew'] = CityTimes.get_current_hebrew_date_words()
    times_data['current_date_english'] = CityTimes.get_current_english_date_words()
    times_data['is_friday'] = CityTimes.is_friday()
    times_data['candle_lighting'] = CityTimes.candle_lighting()
    return times_data


def index(selected_city="Cape Town", date_offset=0):
    city = selected_city or "Cape Town"
    times_data = get_times_data(city, date_offset)
    cities_list = read_cities_from_csv('cities.csv')
    return render_template('times.html', **times_data, city=city, cities=cities_list)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5431)
