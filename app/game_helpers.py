import string
import time
from secrets import choice
import enchant
import flask
from flask import request, redirect, session
import cachetools
from threading import Thread, Lock

from app.levels import get_level

games_mutex = Lock()
dictionary = enchant.Dict("en_US")


def lock_game_and_run(method, *args):
    games_mutex.acquire()
    try:
        return method(*args)
    finally:
        games_mutex.release()
    return


def advance_game(game_name):
    return lock_game_and_run(advance_game_unsafe, game_name)


def advance_game_unsafe(game_name):
    game = get_game(game_name)
    index = game["level_index"]
    game['start_time'] = time.time()
    game['level_index'] = index + 1
    game['level'] = get_level(index + 1)
    game['words'] = []
    game['found_words'] = []
    get_shared()["games"][game_name] = game


def add_game_if_needed(game_name):
    return lock_game_and_run(add_game_if_needed_unsafe, game_name)


def add_game_if_needed_unsafe(game_name, level=None):
    if level is None:
        level = get_level(1)

    shared = get_shared()
    if "games" not in shared:
        shared["games"] = {}
    if game_name not in shared["games"]:
        shared["games"][game_name] = {"name": game_name,
                                      'level': level,
                                      'level_index': 1,
                                      'start_time': time.time()}
    set_shared(shared)


def get_game(game_name):
    shared = get_shared()
    if "games" not in shared:
        return
    if game_name in shared["games"]:
        return shared["games"][game_name]
    return


def get_player_cache():
    # players list max out at 2000 players with 10 minutes of usage
    # plays can continue to play but we will never put more than 2000
    # in the UI for now
    return cachetools.TTLCache(maxsize=2000, ttl=60*10)


def player_active(game_name, name):
    return lock_game_and_run(player_active_unsafe, game_name, name)


def player_active_unsafe(game_name, name):
    game = get_game(game_name)
    if "players" not in game:
        game["players"] = get_player_cache()
    # increase player timeout by setting the name again
    game["players"][name] = name
    get_shared()["games"][game_name] = game


def join_game(game_name, name):
    return lock_game_and_run(join_game_unsafe, game_name, name)


def join_game_unsafe(game_name, name):
    game = get_game(game_name)
    if "players" not in game:
        game["players"] = get_player_cache()
    game["players"][name] = name
    get_shared()["games"][game_name] = game


def get_name():
    if "user_name" in session:
        name = session["user_name"]
    else:
        name = random_name()

    user = {'username': name}
    return name, user


def get_game_name():
    if "game" in request.args:
        name = request.args["game"]
    if "game" in request.form:
        name = request.form["game"]

    game = {'title': name}
    return name, game


def add_game_word(game_name, word, player):
    return lock_game_and_run(add_word_unsafe, game_name, word, player)


def add_word_unsafe(game_name, word, player):
    word = word.strip().lower()

    game = get_game(game_name)

    if not game:
        print("unable to find game and add word:" + game_name)
        return None
    if "words" not in game:
        game["words"] = []
        game["found_words"] = []

    valid_words = game["level"]['valid']
    invalid_words = game["level"]['valid']

    if word not in game["found_words"]:
        valid = word in valid_words         # this is a good word
        invalid = word in invalid_words     # this is a known bad word
        in_dict = dictionary.check(word)    # this word is in the dictionary
        if valid or invalid or in_dict:
            game["words"].append({'text': word, 'valid': valid, 'player': player})
            game["found_words"].append(word)
            return {"valid": valid}
        else:
            return {'invalid': 'unknown word ' + word}
    else:
        return {'invalid': 'word already listed'}

    get_shared()["games"][game_name] = game
    return {"valid": False}


def random_name():
    firsts = ["agent", "dr.", "adjudicator", "prof.", "sgt.", "fank", "sir.", "rebellious", "snidely",
              "happy", "pouty", "sparky", "great", "pinky", "radical", "rotten", "shifty", "stanky", "flunky"]
    seconds = ["dog", "kitty", "bat", "ratatat", "capybara", "mcFrisky", "panda", "kangaroo", "turtle", "bun-bun", "porcupine"]
    first = choice(firsts)
    second = choice(seconds)
    return first.capitalize() + " " + second.capitalize()


def random_game():
    firsts = ["moon", "space_station", "outer_rim_o",
              "ocean_word", "planet", "solar_system",
              "town_o", "island", "black_hole", "hamlet_o",
              "forest_moon", "space", "new", "new_old",
              "old_new"]
    seconds = [
               "words", "nouns", "gerunds", "gerunds",
               "adverbia", "conjunctions", "interjections"]
    first = choice(firsts)
    second = choice(seconds)
    return first + "_" + second


def get_shared():
    if not hasattr(flask.current_app, 'shared'):
        set_shared({})
    return flask.current_app.shared


def set_shared(shared):
    flask.current_app.shared = shared
