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


def get_times_data(city, date_offset):
    times_data = {}
    times_data['dawn'] = Times.dawn(city, date_offset)
    times_data['earliest_tallit'] = Times.earliest_tallit_tefillin(city, date_offset)
    times_data['sunrise'] = Times.sunrise(city, date_offset)
    times_data['latest_shema'] = Times.latest_shema(city, date_offset)
    times_data['latest_shacharit'] = Times.latest_shacharit(city, date_offset)
    times_data['midday'] = Times.midday(city, date_offset)
    times_data['earliest_mincha'] = Times.earliest_mincha(city, date_offset)
    times_data['mincha_ketana'] = Times.mincha_ketana(city, date_offset)
    times_data['plag_hamincha'] = Times.plag_hamincha(city, date_offset)
    times_data['sunset'] = Times.sunset(city, date_offset)
    times_data['nightfall'] = Times.nightfall(city, date_offset)
    times_data['midnight'] = Times.midnight(city, date_offset)
    times_data['shaah_zmanit'] = round(Times.shaah_zmanit(city, date_offset) * 60, 2)
    times_data['current_date_hebrew'] = Times.get_current_hebrew_date_words(city, date_offset)
    times_data['current_date_english'] = Times.get_current_english_date_words(city, date_offset)
    times_data['is_friday'] = Times.is_friday(city, date_offset)
    times_data['candle_lighting'] = Times.candle_lighting(city, date_offset)
    return times_data

def index(selected_city="Cape Town", date_offset=0):
    city = selected_city or "Cape Town"
    times_data = get_times_data(city, date_offset)
    cities_list = read_cities_from_csv('cities.csv')
    return render_template('times.html', **times_data, city=city, cities=cities_list)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
