# During my recent encounter on an article about the vulnerability of weak passwords, I was enlightened on the dangers of weak passwords, which includes single-handedly serving as the "weakest link" to a web server. In details, if my weak password is guessed by an hacker, the whole web server of the site is vulnerable.

# Olu Gbadebo
# Aug 21st 2017
# Password Generator: generates specifically rendom passwords.

# Each password generated as a format (this helps me to remember the password):
# 1: a digit, a randomized-case word, a special character, another word, another special character, a third word, a third special character, one last word, second digit
# 2: a special character, a randomized-case word, a digit, another word, another digit, third word, third digit, last word, special character
# 3: a randomized-case word, a digit, another word, another digit, third word, third digit, last word
# 4: a randomized-case word, a special character, another word, another special character, third word, third special character, last word

# imports
import os
import sys
import random
import warnings
import linecache

# range of digits
DIGITS = [0, 9]
# range of special characters (ascii)
CHARACTERS = [33, 47]

# list of words
DICTIONARY = []

# randomizers
# returns a digit
def randomize_digit(dig_range):
    return random.randint(dig_range[0], dig_range[1])

# retuns a word with varied cases
def randomize_case():
    random_word = get_word()
    result_word = ''
    for every_character in random_word:
        # frequency of capitalizing a every_character
        if (random.randint(0,4) == 1):
            result_word += str(every_character).upper()
        else:
            result_word += every_character
    return result_word

# returns a special character
def randomize_character(char_range):
    if (char_range[0] >= 33 and char_range[1] <= 47):
        return chr(random.randint(char_range[0], char_range[1]))
    else:
        raise ValueError('Invalid special character range')

# get a random word from list of most common words
def get_word():
    if len(DICTIONARY) is not 0:
        return DICTIONARY[random.randint(0, len(DICTIONARY) - 1)]
    # get a word from a random line in dictionary.txt and remove the trailing white space
    try:
        d = open('dictionary.txt', 'r')
    except Exception as e:
        raise Exception("Dictionary file open failed")
    else:
        return linecache.getline('dictionary.txt', random.randint(1, 8829)).split()[0]

# populate with default ranges
def populate_digit(dig_range):
    if len(dig_range) is not 2:
        raise ValueError('Insufficient or excessive digit range array provided')
    if dig_range[0] >= 0 and dig_range[1] <= 9:
        DIGITS[0] = int(dig_range[0])
        DIGITS[1] = int(dig_range[1])
    else:
        raise ValueError('Invalid range for digits')

def populate_char(char_range):
    if len(char_range) is not 2:
        raise ValueError('Insufficient or excessive special characters range array provided')
    if char_range[0] >= 33 and char_range[1] <= 47:
        CHARACTERS[0] = int(char_range[0])
        CHARACTERS[1] = int(char_range[1])
    else:
        raise ValueError('Invalid ascii range for special characters')

def populate_dict(dictionary):
    # empty current dictionary
    del DICTIONARY[:]
    # populate dictionarywith new words
    for every_word in dictionary:
        DICTIONARY.append(every_word)

def create_password():
    # randomly select a format
    pw_type = random.randint(1, 4)
    if pw_type == 1:
        return password_style_1()
    elif pw_type == 2:
        return password_style_2()
    elif pw_type == 3:
        return password_style_3()
    else:
        return password_style_4()

# create password
def password_style_1():
    # 1: a digit, a randomized-case word, a special character, another word, another special character, a third word, a third special character, one last word, second digit
    return str(randomize_digit(DIGITS)) + randomize_case() + randomize_character(CHARACTERS) + randomize_case() + randomize_character(CHARACTERS) + randomize_case() + randomize_character(CHARACTERS) + randomize_case() + str(randomize_digit(DIGITS))

def password_style_2():
    # 2: a special character, a randomized-case word, a digit, another word, another digit, third word, third digit, last word, special character

    return randomize_character(CHARACTERS) + randomize_case() + str(randomize_digit(DIGITS)) + randomize_case() + str(randomize_digit(DIGITS)) + randomize_case() + str(randomize_digit(DIGITS)) + randomize_case() + randomize_character(CHARACTERS)

def password_style_3():
    # 3: a randomized-case word, a digit, another word, another digit, third word, third digit, last word

    return randomize_case() + str(randomize_digit(DIGITS)) + randomize_case() + str(randomize_digit(DIGITS)) + randomize_case() + str(randomize_digit(DIGITS)) + randomize_case()

def password_style_4():
    # 4: a randomized-case word, a special character, another word, another special character, third word, third special character, last word

    return randomize_case() + randomize_character(CHARACTERS) + randomize_case() + randomize_character(CHARACTERS) + randomize_case() + randomize_character(CHARACTERS) + randomize_case()

def run(dictionary=None, dig_range=None, char_range=None):
    try:
        if dictionary is None and dig_range is None and char_range is None:
            return create_password()
        # warnings.warn('Parameters not provided will be replaced with default values.')
        if dictionary:
            populate_dict(dictionary)
        if dig_range:
            populate_digit(dig_range)
        if char_range:
            populate_char(char_range)
    except Exception as error:
        raise error
    else:
        return create_password()

if __name__ == '__main__':
    print( run() )
