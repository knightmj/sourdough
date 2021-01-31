import json

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
    file = "static/level" + str(i) + ".json"
    with app.open_resource(file) as f:
        return json.load(f)
