import string
import re
import .letter
import .number_cruncher
class Person(object):
    pass
    def __init__(self, name, dob):
        self.numbers = {}
        self.raw_name_input = name
        self.raw_date_input = dob
        self.cleaned_name = raw_name_input.strip()
        for char in cleaned_name:
            #cleaned_name preserves capitalization and some formatting for display
            #letters, apostrophes, hyphens, and spaces get a pass
            #as they are used in names. Periods and commas are removed.
            #exclamation points are used to indicate a switch between consonant
            #and vowel i.e., when 'y' makes a vowel sound
            if char in ('!',"'",'-', ' ') or char in string.ascii_letters:
                pass
            else:
                cleaned_name = cleaned_name.replace(char, "")
        cleaned_name = re.sub('\s+', ' ', cleaned_name)
