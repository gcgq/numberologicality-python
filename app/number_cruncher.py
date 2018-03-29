from app.letter import Letter


MASTER_NUMBERS = [11, 22, 33]
PARSE_NAMES_INDIVIDUALLY = True
REDUCE_MN = False


def process_name_string(input, key):
    if PARSE_NAMES_INDIVIDUALLY:
        names = input.split(" ")
    else:
        names = list(input.replace(" ", ""))
    letter_counts = [tally_letters(name) for name in names]
    result = [count[key] for count in letter_counts]
    return result


def tally_letters(input=""):
    # sorts the input into dictionaries of consonants and vowels
    total_count, vowel_count, consonant_count = {}, {}, {}
    name_chars = list(input.lower())
    # print(name_chars)
    for i in range(len(name_chars)):
        l = Letter(name_chars[i])
        if name_chars[i] in ('!', "'", '-'):
            pass
        elif l.is_letter() is False:
            print("{} is not a letter. check input".format(name_chars[i]))
        else:
            total_count = tally(total_count, l.letter)
            if l.is_consonant():
                if name_chars[i - 1] is '!':
                    vowel_count = tally(vowel_count, l.letter)
                else:
                    consonant_count = tally(consonant_count, l.letter)
            elif l.is_vowel():
                if name_chars[i - 1] is '!':
                    consonant_count = tally(consonant_count, l.letter)
                else:
                    vowel_count = tally(vowel_count, l.letter)
            else:
                print("this shouldn't be a thing")
    # print("tc:{}\ncc:{}\nvc:{}\n".format(total_count, consonant_count, vowel_count))
    return {"all": total_count,
            "consonants": consonant_count,
            "vowels": vowel_count}


def tally(d, letter):
    if letter in d.keys():
        d[letter] += 1
    else:
        d[letter] = 1
    return d


def tabulate(ary):
    # names are supposed to be calclated individually, so the results will
    # be stored in an array before the final number is summed and reduced
    # if the more straightforward whole name approach is desired, that could be
    # implemented in other methods that pass a single name to this method
    results = []
    for letter_dict in ary:
        r = 0
        for key in letter_dict.keys():
            k = Letter(key)
            r += k.get_value() * letter_dict[key]
        results.append(reduce(r))
    return reduce(sum(results))


def reduce(num):
    result = 0
    reduce_master_numbers = REDUCE_MN
    if reduce_master_numbers is False and num in MASTER_NUMBERS:
        return num
    else:
        while(num > 0):
            result += num % 10
            num //= 10
        if(reduce_master_numbers is False and result in MASTER_NUMBERS):
            return result
        elif(result < 10):
            return result
        else:
            return reduce(result)


def date_of_birth_number(date, method=0):
    # date is the PersonData.dob of a given person.
    # date is a datetime object and can be manipulated as such
    result = 0
    if method is 0:
        for num in date.date().isoformat().split('-'):
            result += reduce(int(num))
        result = reduce(result)
    else:
        result = reduce(int(''.join(date.split('-'))))
    return result


def full_name_number(name):
    all_letters = process_name_string(name, 'all')
    return tabulate(all_letters)


def consonant_number(name):
    consonants = process_name_string(name, 'consonants')
    return tabulate(consonants)


def vowel_number(name):
    vowels = process_name_string(name, 'vowels')
    return tabulate(vowels)


def pinnacles(dob):
    # First Pinnacle = Month of Birth + Day of Birth
    # Second Pinnacle = Day of Birth + Year of Birth
    # Third Pinnacle = First Life Stage Number + Second Life Stage Number
    # Fourth Pinnacle = Month of Birth + Year of Birth
    p1 = reduce((dob.month + dob.day))
    p2 = reduce((dob.day + dob.year))
    p3 = reduce((p1 + p2))
    p4 = reduce((dob.month + dob.year))
    return (p1, p2, p3, p4)


def challenges(dob):
    # First Challenge Number = Day of Birth – Month of Birth
    # Second Challenge Number = Year of Birth – Day of Birth
    # Third Challenge Number = Second Challenge Number – First Challenge Number
    # Fourth Challenge Number = Year of Birth – Month of Birth
    c1 = reduce(abs(dob.day - dob.month))
    c2 = reduce(abs(dob.year - dob.day))
    c3 = reduce(abs(c2 - c1))
    c4 = reduce(abs(dob.year - dob.month))
    return (c1, c2, c3, c4)


calculate = {
    'full_name_number': full_name_number,
    'consonant_number': consonant_number,
    'vowel_number': vowel_number,
    'life_path': date_of_birth_number,
    'expression': full_name_number,
    'destiny': full_name_number,
    'personality': consonant_number,
    'hearts_desire': vowel_number,
    'soul_urge': vowel_number,
    'pinnacles': pinnacles,
    'challenges': challenges
}
