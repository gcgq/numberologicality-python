from app import app
from flask import render_template, request
from app.person_data import PersonData
from datetime import date
from random import randint, shuffle
import pyrebase
import config

firebase = pyrebase.initialize_app(config.FIREBASE)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", data=None)


@app.route("/", methods=["POST"])
def submit_form():
    data = request.form
    d = {}
    d['dob'] = data['dob']
    d['name'] = data['name']

    # account for missing data. Remove when form validation works
    if d['name'] is '':
        d['name'] = 'John Doe'
    if d['dob'] is '':
        d['dob'] = date.today().strftime('%m-%d-%Y')

    # process input and retrieve nubers
    person = PersonData(name=d['name'], dob=d['dob'])
    firebase.database().child('/data_from_users').\
        child(firebase.database().generate_key()).\
        set(person.get_json())
    person = person.get_data()
    # retrieve relevant interpretations from config, then pass it to the template
    kindred = get_kindred(person)
    num_interps = {}
    settings = config.get_settings()
    for i in settings['core_numbers']:
        num_interps[i] = config.INTERPRETATIONS[i][str(person['numbers'][i])]
    return render_template("report.html", data=person, ni=num_interps, k=kindred, s=settings)


@app.template_filter('date')
def format_date(date, format="%B %-d, %Y"):
    return date.strftime(format)


def get_kindred(person):
    rnd = randint(0, config.NAME_COUNT - 1000)
    random_slice = firebase.database().\
        child("data_from_wiki").\
        order_by_child("person_id").\
        start_at(rnd).\
        end_at(rnd + 1000).\
        get().val()

    random_slice = list(random_slice.items())
    # print(type(random_slice))
    # print(random_slice)

    kindred = {
        "life_path": [],
        "destiny": [],
        "soul_urge": [],
        "personality": []
    }

    for wiki_item in random_slice:
        for key in ("life_path", "destiny", "soul_urge", "personality"):
            # print(person)
            # print(wiki_item)
            if person["numbers"][key] is wiki_item[1][key]:
                kindred[key].append(wiki_item[1])

    for key in ("life_path", "destiny", "soul_urge", "personality"):
        shuffle(kindred[key])
    return kindred
