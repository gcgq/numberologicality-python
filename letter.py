class Letter(object):
    def __init__(self, l):
        l = l.lower()
        if self.is_letter(l):
            self.letter = l

    values = {
        "pythagorean": {
        ('a','j','s'):1, ('b','k','t'):2, ('c','l','u'):3,
        ('d','m','v'):4, ('e','n','w'):5, ('f','o','x'):6,
        ('g','p','y'):7, ('h','q','z'):8, ('i','r'):9
        },
        "chaldean": {
        ('a','i','j','q','y'):1, ('o','z'):7, ('f','p'):8,
        ('b','k','r'):2, ('d','m','t'):4, ('u','v','w'):6,
        ('c','g','l','s'):3, ('e','h','n','x'):5
        }
    }

    def is_letter(self, ltr=None):
        if ltr is None:
            ltr = self.letter
        import string
        return True if ltr in string.ascii_lowercase else False

    def is_consonant(self):
        return False if self.is_vowel() else True

    def is_vowel(self):
        vowels = ('a','e','i','o','u')
        return True if self.letter in vowels else False

    def get_value(self, type):
        for key in Letter.values[type].keys():
            if self.letter in key:
                return Letter.values[type][key]
