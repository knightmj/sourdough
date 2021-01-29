import uuid
from secrets import choice

import flask
from flask import render_template, make_response
from flask import request, redirect
from app import app
import cachetools


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


def random_name():
    firsts = ["happy", "sad", "good", "great", "orange", "rad", "rotten", "shifty"]
    seconds = ["dog", "cat", "bat", "rat", "kaola", "panda", "kangaroo", "turtle", "bunny", "porcupine"]
    first = choice(firsts)
    second = choice(seconds)
    return "Agent " + first.capitalize() + " " + second.capitalize()


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


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    shared = get_shared
    if not hasattr(shared, 'count'):
        shared.count = 1
    else:
        shared.count = 1 + shared.count

    stats = {"count": shared.count}

    if 'user_uid' not in request.cookies:
        user_id = str(uuid.uuid1())
        name = random_name()
        user = {'username': name}
        resp = make_response(render_template('welcome.html', user=user, stats=stats))
        resp.set_cookie('user_uid', user_id)
        resp.set_cookie('user_name', name)
    else:
        name, user = get_name()
        resp = make_response(render_template('welcome.html', user=user, stats=stats))
        resp.set_cookie('user_name', name)

    return resp


@app.route('/games', methods=["POST", "GET"])
def games():
    if 'user_uid' not in request.cookies:
        return redirect("/index")
    name, user = get_name()

    game = {'random': random_game()}
    game_list = []
    shared = get_shared()
    if "games" in shared:
        game_list = shared["games"].values()

    resp = make_response(render_template('games.html', user=user, game=game, games=game_list))
    return resp


def update_game(game_name):
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
    game = get_game(game_name)
    if "players" not in game:
        game["players"] = cachetools.TTLCache(maxsize=999999, ttl=60 * 20)
    game["players"][name] = name
    get_shared()["games"][game_name] = game


@app.route('/play', methods=["POST", "GET"])
def play():
    if 'user_uid' not in request.cookies:
        return redirect("/index")
    name, user = get_name()
    game_name, game = get_game_name()
    update_game(game_name)
    join_game(game_name, name)
    game = get_game(game_name)
    resp = make_response(render_template('play.html', user=user, game=game, players=game["players"].keys()))
    return resp
