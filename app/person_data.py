import string, unicodedata, re
from dateutil.parser import parse as parse_dob
import number_cruncher as nc
class PersonData(object):
    def __init__(self, name, dob):
        # PersonData(name, dob) gets input from Flask response object, which
        # gets data from from the front-end AJAX GET method
        # name should be a string,
        # dob should be a javascript Date().toUTCString() or Date().toISOString()
        self.numbers = {}
        self.raw_input = { 'name': name, 'dob': dob, 'ignored_characters':[] }
        self.name = self.normalize_name(self.raw_input['name'])
        self.date_of_birth = parse_dob(dob)
    def normalize_name(self, name):
        result = name
        for char in name:
            #clean input, but preserve capitalization and some formatting for display.
            #Letters, apostrophes, hyphens, and spaces get a pass,
            #as they are used in names. Periods and commas are removed.
            #Diacriticals are normalized as ascii characters.
            #exclamation points are used to indicate a switch between consonant
            #and vowel i.e., when 'y' makes a vowel sound
            if char in ('!',"'",'-', ' ') or char in string.ascii_letters:
                pass
            else:
                normalized_char = unicodedata.normalize('NFKD',char) \
                                    .encode('ASCII','ignore') \
                                    .decode('ASCII')
                # print("char: {}, normalized: {}".format(char, normalized_char))
                if len(normalized_char) is not 0 and normalized_char in string.ascii_letters:
                    result = result.replace(char, normalized_char)
                else:
                    self.raw_input['ignored_characters'].append(char)
                    result = result.replace(char, "")
                    result = re.sub('\s+', ' ', result).strip()
        # print("PersonData.normalize_name()")
        # print("input: {}".format(name))
        # print("output: {}".format(result))
        return result
    def process_data(self):
        name_keys = ("destiny","soul_urge","personality")
        date_keys = ("life_path", "pinnacles", "challenges")
        for key in name_keys:
            self.number[key] = nc.calculate[key](self.name)
        for key in date_keys:
            self.number[key] = nc.calculate[key](self.date_of_birth)

    def to_json(self):
        pass
    def post_to_db(self):
        pass
