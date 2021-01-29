import uuid
from secrets import choice

from flask import render_template, make_response
from flask import request, redirect
from app import app


def get_name():
    if "user_name" in request.cookies:
        name = request.cookies["user_name"]
    else:
        name = random_name()
    if "selected_name" in request.form:
        name = request.form["selected_name"]

    user = {'username': name}
    return name, user


def get_game():
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
    firsts = ["planet", "solar system", "town_o_", "island", "black hole"]
    seconds = ["words", "nouns", "gerunds", "gerunds", "adverbia", "conjunctions", "interjections",]
    first = choice(firsts)
    second = choice(seconds)
    return first.capitalize() + "_" + second.capitalize()


@app.route('/', methods=["GET"])
@app.route('/index', methods=["GET"])
def index():
    print(request.cookies.__dict__)

    if 'user_uid' not in request.cookies:
        user_id = str(uuid.uuid1())
        name = random_name()
        user = {'username': name}
        resp = make_response(render_template('welcome.html', user=user))
        resp.set_cookie('user_uid', user_id)
        resp.set_cookie('user_name', name)
        print("setting user id")
    else:
        name, user = get_name()
        resp = make_response(render_template('welcome.html', user=user))
        resp.set_cookie('user_name', name)

    return resp


@app.route('/games', methods=["POST", "GET"])
def games():
    if 'user_uid' not in request.cookies:
        return redirect("/index")
    name, user = get_name()

    game = {'random': random_game()}
    resp = make_response(render_template('games.html', user=user, game=game))
    return resp


@app.route('/play', methods=["POST", "GET"])
def play():
    if 'user_uid' not in request.cookies:
        return redirect("/index")
    name, user = get_name()

    game_name, game = get_game()
    resp = make_response(render_template('play.html', user=user, game=game))
    return resp
