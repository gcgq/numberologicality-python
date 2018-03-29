import json

DEBUG = True
CSRF_ENABLED = True
INTERPRETATIONS = {}
with open('app/static/interpretations.json', 'r') as file:
    INTERPRETATIONS = json.load(file)

# settings to facilitate getting things labelled right in templates
REDUCE_INDIVIDUALLY = True
INCLUDE_PINNACLES = False
INCLUDE_CHALLENGES = False
CORE_NUMBERS = ['life_path', 'destiny', 'soul_urge', 'personality']
OTHER_NUMBERS = ()
HTML_LABELS = {
    'life_path': {'id': 'life',
                  'name': 'Life Path',
                  'bd_str': 'date'},
    'destiny': {'id': 'dest',
                'name': 'Destiny',
                'bd_str': 'all'},
    'soul_urge': {'id': 'soul',
                  'name': 'Soul Urge',
                  'bd_str': 'vowels'},
    'personality': {'id': 'pers',
                    'name': 'Personality',
                    'bd_str': 'consonants'},
    'pinnacles': {'id': 'pinn',
                  'name': 'Pinnacle',
                  'bd_str': 'date_p'},
    'challenges': {'id': 'chal',
                   'name': 'Challenge',
                   'bd_str': 'date_c'}
}

FIREBASE = {
    "apiKey": "AIzaSyBirgFENs1QxHbrhxQpNX3uDnjB4RKtZE0",
    "authDomain": "numberologicali.firebaseapp.com",
    "databaseURL": "https://numberologicali.firebaseio.com",
    "projectId": "numberologicali",
    "storageBucket": "numberologicali.appspot.com",
    "messagingSenderId": "573631785187"
}
NAME_COUNT = 30162 - 1


def get_settings():
    settings = {}
    settings['core_numbers'] = CORE_NUMBERS
    settings['labels'] = HTML_LABELS
    if INCLUDE_PINNACLES:
        settings['pinnacles'] = True
    if INCLUDE_CHALLENGES:
        settings['challenges'] = True
    return settings
