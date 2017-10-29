master_numbers = [11,22,33]
def parse_name(input=""):
    total_count, vowel_count, consonant_count = {}, {}, {}

    name_chars = list(input.lower().strip(" \s\t\r"))
    #print(name)

def reduce(num, reduce_master_numbers=True):
    result = 0
    while(num > 0):
        result += num % 10
        num //= 10
        if(reduce_master_numbers is False and result in master_numbers):
            return result
        elif(result > 10):
            return result
        else:
            return reduce(result, reduce_master_numbers)

def life_path(date, reduce_master_numbers, method=0):
    #date is the PersonData.dob of a given person.
    #date is a datetime object and can be manipulated as such
    result = 0
    rmn = reduce_master_numbers
    if method is 0:
        result = reduce(reduce(date.year, rmn)+reduce(date.month, rmn)+reduce(date.day, rmn))
    else:
        result = reduce((date.year + date.month + date.day), rmn)
    return result

def expression():
    pass
def destiny():
    pass
    # result = {raw_total=0,}
def hearts_desire():
    pass
def souls_urge():
    pass
def personality():
    pass
def pinnacle():
    pass
def challenge():
    pass
