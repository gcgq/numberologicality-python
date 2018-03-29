from app.person_data import PersonData
import pyrebase
import config
import json
from dateutil.parser import parse

firebase = pyrebase.initialize_app(config.FIREBASE)


def import_data(file):
    data_from_json = []

    with open(file, 'r') as json_data:
        data_from_json = [json.loads(item) for item in json_data.readlines()]

    processed_data = []
    person_id = 0
    for item in data_from_json:
        if item['insufficient_data'] is False:
            new_item = PersonData(item['full_name'], item['birth']).get_data()
            for key in ["url", "public_name", "occupation", "death"]:
                try:
                    new_item[key] = item[key]
                    if key is "death":
                        new_item[key] = parse(new_item[key]).date().isoformat()
                except KeyError:
                    new_item[key] = None
            # json_data = json.dumps({
            #     'name': new_item['name'],
            #     'public_name': new_item['public_name'],
            #     'occupation': new_item['occupation'],
            #     'dob': new_item['dob'].date().isoformat(),
            #     'death': new_item['death'],
            #     'life_path': new_item['numbers']['life_path'],
            #     'destiny': new_item['numbers']['destiny'],
            #     'soul_urge': new_item['numbers']['soul_urge'],
            #     'personality': new_item['numbers']['personality'],
            #     'pinnacles': new_item['numbers']['pinnacles'],
            #     'challenges': new_item['numbers']['challenges'],
            #     'bd_str': new_item['breakdown']['all'],
            #     'url': new_item['url']
            #     # 'input': new_item['raw_input']
            # })
            # print(json_data)
            if new_item['numbers']['life_path'] is 0 or\
                    new_item['numbers']['destiny'] is 0 or\
                    new_item['numbers']['soul_urge'] is 0 or\
                    new_item['numbers']['personality'] is 0:
                pass
            else:
                flatten_data = {
                    'name': new_item['name'],
                    'public_name': new_item['public_name'],
                    'occupation': new_item['occupation'],
                    'dob': new_item['dob'].date().isoformat(),
                    'death': new_item['death'],
                    'life_path': new_item['numbers']['life_path'],
                    'destiny': new_item['numbers']['destiny'],
                    'soul_urge': new_item['numbers']['soul_urge'],
                    'personality': new_item['numbers']['personality'],
                    'pinnacles': new_item['numbers']['pinnacles'],
                    'challenges': new_item['numbers']['challenges'],
                    'bd_str': new_item['breakdown']['all'],
                    'url': new_item['url'],
                    'person_id': person_id
                }
                processed_data.append(flatten_data)
                person_id += 1
    for person in processed_data:
        firebase.database().child('/data_from_wiki').push(person)


import_data("scraper-data.json")
