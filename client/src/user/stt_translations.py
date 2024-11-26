import re

moves_translations = {
    """Corrects and standardizes the recognized command text for chess moves."""
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "he": "e",
    "if": "f",
    "te": "d",
    "for": "4",
    "fine": "5",
    "flight": "5",
    "fight": "5",
    "fly": "5",
    "want": "1",
    "to": "2",
    "aid": "8",
    "the": "b",
    "be": "b",
    "too": "2",
    "before": "b4",
    "basics": "b5",
    "si": "c",
    "see": "c",
    "seed": "c8",
    "do you": "d",
    "day": "d",
    "did": "d",
    "di": "d",
    "won": "1",
    "is": "e",
    "ate": "8",
    "as": "f",
    "gee": "g",
    "jade": "g8",
    "aged": "h",
    "age": "h",
    "ha it": "h8",
    "ches": "chess",
    "what": "",
    "it": "",
    "defy": "d5",
    "one": "1",
}


def correct_recognition(text):

    for word, replacement in moves_translations.items():
        text = re.sub(r"\b" + word + r"\b", replacement, text)

    return text
