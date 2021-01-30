import uuid
from flask import render_template, make_response, jsonify
from app import app
from app.game_helpers import *


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


@app.route('/play', methods=["POST", "GET"])
def play():
    set_cookie = False
    if 'user_uid' not in request.cookies:
        user_id = str(uuid.uuid1())
        set_cookie = True
    name, user = get_name()
    game_name, game = get_game_name()
    add_game_if_needed(game_name)
    join_game(game_name, name)
    game = get_game(game_name)
    resp = make_response(render_template('play.html', user=user, game=game, players=game["players"].keys()))
    if set_cookie:
        resp.set_cookie('user_uid', user_id)
        resp.set_cookie('user_name', name)
    return resp


@app.route('/add_word', methods=["GET"])
def add_word():
    if "word" not in request.args or "game" not in request.args:
        return "Invalid args", 400

    result = add_game_word(request.args["game"],  request.args["word"])
    return jsonify(result)
