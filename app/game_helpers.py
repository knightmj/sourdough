import string
from secrets import choice
import enchant
import flask
from flask import request, redirect
import cachetools
from threading import Thread, Lock

games_mutex = Lock()
dictionary = enchant.Dict("en_US")

def lock_game_and_run(method, *args):
    games_mutex.acquire()
    try:
        return method(*args)
    finally:
        games_mutex.release()
    return


def add_game_if_needed(game_name):
    return lock_game_and_run(add_game_if_needed_unsafe, game_name)


def add_game_if_needed_unsafe(game_name):
    shared = get_shared()
    if "games" not in shared:
        shared["games"] = {}
    if game_name in shared["games"]:
        # update for ttl
        shared["games"][game_name] = shared["games"][game_name]
    else:
        shared["games"][game_name] = {"name": game_name}
    set_shared(shared)


def get_game(game_name):
    shared = get_shared()
    if "games" not in shared:
        return
    if game_name in shared["games"]:
        return shared["games"][game_name]
    return


def join_game(game_name, name):
    return lock_game_and_run(join_game_unsafe, game_name, name)


def join_game_unsafe(game_name, name):
    game = get_game(game_name)
    if "players" not in game:
        game["players"] = cachetools.TTLCache(maxsize=999999, ttl=60 * 20)
    game["players"][name] = name
    get_shared()["games"][game_name] = game


def get_name():
    if "user_name" in request.cookies:
        name = request.cookies["user_name"]
    else:
        name = random_name()
    if "selected_name" in request.form:
        name = request.form["selected_name"]

    user = {'username': name}
    return name, user


def get_game_name():
    if "game" in request.args:
        name = request.args["game"]
    if "game" in request.form:
        name = request.form["game"]

    game = {'title': name}
    return name, game


def add_game_word(game_name, word):
    return lock_game_and_run(add_word_unsafe, game_name, word)


def add_word_unsafe(game_name, word):
    word = word.strip()

    if not dictionary.check(word):
        return {"invalid": "word is not in dictionary"}

    game = get_game(game_name)
    if not game:
        print("unable to find game and add word:" + game_name)
        return None
    if "words" not in game:
        game["words"] = []

    if word not in game["words"]:
        game["words"].append(word)

    get_shared()["games"][game_name] = game
    return {"valid": True}


def random_name():
    sirs = ["Agent", "Dr.", "Adjudicator"]
    firsts = ["happy", "sad", "good", "great", "pink", "rad", "rotten", "shifty", "stanky"]
    seconds = ["dog", "cat", "bat", "rat", "kaola", "panda", "kangaroo", "turtle", "bunny", "porcupine"]
    sir = choice(sirs)
    first = choice(firsts)
    second = choice(seconds)
    return sir.capitalize() + " " + first.capitalize() + " " + second.capitalize()


def random_game():
    firsts = ["planet", "solar_system", "town_o", "island", "black_hole", "hamlet_o", "forest_moon", "space"]
    seconds = ["words", "nouns", "gerunds", "gerunds", "adverbia", "conjunctions", "interjections"]
    first = choice(firsts)
    second = choice(seconds)
    return first + "_" + second


def get_shared():
    if not hasattr(flask.current_app, 'shared'):
        set_shared({})
    return flask.current_app.shared


def set_shared(shared):
    flask.current_app.shared = shared
