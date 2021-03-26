import json
import math
import random

from app import app

levelx = {
    "board": [
        [
            "Z",
            "A",
            "R"
        ],
        [
            "I",
            "Z",
            "D"
        ],
        [
            "L",
            "P",
            "E"
        ]
    ],
    "valid": [
        "adz",
        "adze",
        "darzi",
        "daze",
        "izar",
        "izard",
        "izzard",
        "lizard",
        "piazze",
        "pize",
        "pized",
        "pizza",
        "raze",
        "razed",
        "razz",
        "razzed",
        "zed",
        "zep",
        "zip",
        "ziz"
    ],
    "invalid": [
        "ail",
        "ard",
        "drail",
        "liar",
        "liard",
        "lip",
        "lipe",
        "ped",
        "pedrail",
        "pia",
        "rad",
        "rade",
        "rai",
        "rail"
    ],
    "required": [
        "lizard"
    ],
    "rule_text": "Must contain the letter z",
    "number_of_words": 7,
    "time_s": 180,
    "text_fully_revealed_at_s": 90
}


def get_level(i):
    boards = 7896
    levels = 250
    boards_per_level = boards/levels
    index = math.floor(random.randint(1, math.floor(boards_per_level)) + boards_per_level * (i-1))
    print("loading board", index)
    file = "static/generated_boards/" + str(index) + ".json"
    with app.open_resource(file) as f:
        return json.load(f)
