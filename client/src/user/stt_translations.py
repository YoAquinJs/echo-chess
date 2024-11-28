"""
This module provides a mapping for correcting recognition errors in chess moves
and functions to process recognized text.
"""

import re


moves_translations = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "if": "F",
    "te": "D",
    "for" : "4",
    "fine" : "5",
    "want" : "1",
    "to" : "2",
    "aid" : "8",
    "the" : "D",
    "be" : "B",
    "too" : "2",
    "before" : "B 4",
    "basics" : "B 5",
    "si" : "C",
    "see" : "C",
    "seed" : "C 8",
    "do you" : "D",
    "day" : "D",
    "did" : "d 8",
    "won" : "1",
    "is" : "E",
    "ate" : "8",
    "as" : "F",
    "jade" : "G 8",
    "aged" : "H",
    "ha it" : "H 8",
    "ches" : "chess",
    "what": "",
    "hey": "A",
    "sea": "C",
    "dee": "D",
    "he": "E",
    "eff": "F",
    "gee": "G",
    "age": "H",
    "cheers": "chess",
    "chest": "chess",
    "chests" : "chess",
    "chance" : "chess",
    "jess" : "chess",
    "jes": "chess",
    "just": "chess",
    "chez" : "chess",
    "warned" : "1",
    "file" : "5",
    "you" : "2",
    "defy" : "D5",
    "beef" : "B",
    "fi" : "5",
    "true" : "2",
    "worn" : "one",
    " ": "",


}


def correct_recognition(text: str) -> str:
    """
    Corrects recognition errors using predefined translations.
    """
    for word, replacement in moves_translations.items():
        text = re.sub(r'\b' + re.escape(word) + r'\b', replacement, text, flags=re.IGNORECASE)
    return text

def filter_move(input_str: str) -> str:
    """
    Validates and formats chess moves (e.g., 'B 1 to C 4' -> 'B1C4').
    """

    input_str = input_str.replace(" ", "").upper()

   
    valid_letters = "ABCDEFGH"
    valid_numbers = "12345678"


    filtered = "".join(c for c in input_str if c in valid_letters or c in valid_numbers)

    if len(filtered) == 4 and filtered[0] in valid_letters and filtered[1] in valid_letters \
            and filtered[2] in valid_numbers and filtered[3] in valid_numbers:
        return filtered

    return "Invalid move format"














