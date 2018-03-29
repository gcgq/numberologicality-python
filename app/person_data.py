import string
import unicodedata
import re
import json
import config
from dateutil.parser import parse as parse_dob
import app.number_cruncher as nc
from app.letter import Letter


class PersonData(object):
    def __init__(self, name, dob):
        # PersonData(name, dob) gets input from Flask response object
        # name should be a string,
        # dob should be a javascript Date().toUTCString() or Date().toISOString()
        self.raw_input = {'name': name, 'dob': dob, 'ignored_characters': []}
        self.name = self._normalize_name(self.raw_input['name'])
        self.date_of_birth = parse_dob(dob)
        self.numbers = self._generate_numbers()
        self.breakdown_strings = self._format_breakdown_strings()

    def _normalize_name(self, name):
        result = name
        for char in name:
            # clean input, but preserve capitalization and some formatting for display.
            # Letters, apostrophes, hyphens, and spaces get a pass,
            # as they are used in names. Periods and commas are removed.
            # Diacriticals are normalized as ascii characters.
            # exclamation points are used to indicate a switch between consonant
            # and vowel i.e., when 'y' makes a vowel sound
            if char in ('!', "'", '-', ' ') or char in string.ascii_letters:
                pass
            else:
                normalized_char = unicodedata.normalize('NFKD', char) \
                    .encode('ASCII', 'ignore') \
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

    def _generate_numbers(self):
        num = {}
        name_keys = ("destiny", "soul_urge", "personality")
        date_keys = ("life_path", "pinnacles", "challenges")
        for key in name_keys:
            num[key] = nc.calculate[key](self.name)
        for key in date_keys:
            if key is not 'life_path':
                nc.REDUCE_MN = True
                num[key] = nc.calculate[key](self.date_of_birth)
                nc.REDUCE_MN = False
            else:
                num[key] = nc.calculate[key](self.date_of_birth)
        self.name = self.name.replace('!', '')
        return num

    def _format_breakdown_strings(self):
        bd = {'all': ['', ''],
              'vowels': ['', ''],
              'consonants': ['', ''],
              'date': ['', '']}
        name_chars = list(self.name.lower())
        # print(name_chars)
        for i in range(len(name_chars)):
            l = Letter(name_chars[i])
            if name_chars[i] in ('!', "'", '-', " "):
                pass
            elif not l.is_letter():
                print("{} is not a letter. check input".format(name_chars[i]))
            else:
                bd['all'][0] += l.letter
                bd['all'][1] += str(l.get_value())
                if l.is_consonant():
                    if name_chars[i - 1] is '!':
                        bd['vowels'][0] += l.letter
                        bd['vowels'][1] += str(l.get_value())
                        bd['consonants'][0] += ' '
                        bd['consonants'][1] += ' '

                    else:
                        bd['consonants'][0] += l.letter
                        bd['consonants'][1] += str(l.get_value())
                        bd['vowels'][0] += ' '
                        bd['vowels'][1] += ' '

                elif l.is_vowel():
                    if name_chars[i - 1] is '!':
                        bd['consonants'][0] += l.letter
                        bd['consonants'][1] += str(l.get_value())
                        bd['vowels'][0] += ' '
                        bd['vowels'][1] += ' '
                    else:
                        bd['vowels'][0] += l.letter
                        bd['vowels'][1] += str(l.get_value())
                        bd['consonants'][0] += ' '
                        bd['consonants'][1] += ' '
                else:
                    print("this shouldn't be a thing")
        # 12/22/1222
        bd['date'][0] = "{}/{}/{}".format(self.date_of_birth.day,
                                          self.date_of_birth.month,
                                          self.date_of_birth.year)
        # 3 + 4 + 7
        if config.REDUCE_INDIVIDUALLY:
            bd['date'][1] = "{} + {} + {}".format(nc.reduce(self.date_of_birth.day),
                                                  nc.reduce(self.date_of_birth.month),
                                                  nc.reduce(self.date_of_birth.year))
        # 1+2+2+2+1+2+2+2
        else:
            bd['date'][1] = '+'.join(list("{}{}{}".format(self.date_of_birth.day,
                                                          self.date_of_birth.month,
                                                          self.date_of_birth.year)))

        return bd

    def get_data(self):
        return {
            'name': self.name,
            'dob': self.date_of_birth,
            'numbers': self.numbers,
            'input': self.raw_input,
            'breakdown': self.breakdown_strings
        }

    def get_json(self):
        json_data = json.dumps({
            'name': self.name,
            'dob': self.date_of_birth.date().isoformat(),
            'life_path': self.numbers['life_path'],
            'destiny': self.numbers['destiny'],
            'soul_urge': self.numbers['soul_urge'],
            'personality': self.numbers['personality'],
            'pinnacles': self.numbers['pinnacles'],
            'challenges': self.numbers['challenges'],
            'input': self.raw_input,
            'bd_str': self.breakdown_strings['all']
        })
        # print(json_data)
        return json_data
