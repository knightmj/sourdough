import uuid
from flask import render_template, make_response, jsonify, session
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

    if 'user_uid' not in session:
        name = random_name()
        user = {'username': name}
        session["user_name"] = name
        resp = make_response(render_template('welcome.html', user=user, stats=stats))
        return resp
    else:
        name, user = get_name()
        if "new" in request.args:
            name = random_name()
        session["user_name"] = name

        resp = make_response(render_template('welcome.html', user=user, stats=stats))

        return resp


@app.route('/games', methods=["POST", "GET"])
def games():
    name, user = get_name()

    game = {'random': random_game()}

    resp = make_response(render_template('games.html', user=user, game=game))

    return resp


@app.route('/game_list', methods=["POST", "GET"])
def game_list():
    all_games = []
    shared = get_shared()
    if "games" in shared:
        all_games = shared["games"].values()

    resp = make_response(render_template('game_list.html', games=all_games))
    return resp


@app.route('/play', methods=["POST", "GET"])
def play():
    name, user = get_name()

    if "user_name" not in session:
        session["user_name"] = name

    game_name, game = get_game_name()
    add_game_if_needed(game_name)
    join_game(game_name, name)
    game = get_game(game_name)
    image = "/static/" + game["level"]["background_image"]

    resp = make_response(render_template('play.html', user=user,
                                         board=game['level']['board'],
                                         game=game,
                                         link=request.url,
                                         background_image=image,
                                         players=game["players"].keys()))
    return resp


@app.route('/add_word', methods=["GET"])
def add_word():
    if "word" not in request.args or "game" not in request.args \
            or "player" not in request.args:
        return "Invalid args", 400

    result = add_game_word(request.args["game"], request.args["word"], request.args["player"])
    return jsonify(result)


@app.route('/get_game_data', methods=["GET"])
def get_game_data():
    if "game" not in request.args:
        return "Invalid args", 400
    game = get_game(request.args["game"])
    start_time = game["start_time"]
    elapsed = time.time() - start_time
    reveal_time = game["level"]["text_fully_revealed_at_s"]
    total_time = game["level"]["time_s"]
    remaining_time = total_time - elapsed
    if remaining_time < 0:
        remaining_time = 0

    if "words" not in game:
        game["words"] = []
        game["found_words"] = []

    valid = 0
    for word in game["words"]:
        if word["valid"]:
            valid = valid + 1

    remaining_words = game["level"]["number_of_words"] - valid

    percent_text = elapsed / reveal_time
    letters = int(percent_text * len(game["level"]["rule_text"]))
    extra = len(game["level"]["rule_text"]) - letters
    extra /= 2
    text = game["level"]["rule_text"][:letters] + int(extra) * "* "

    if remaining_words == 0:
        advance_game(request.args["game"])
    players = []
    for player in game["players"].keys():
        players.append(str(player))

    data = {
        'players': players,
        'remaining_words': remaining_words,
        'remaining_time': remaining_time,
        'rule_text': text,
        'level_index': game["level_index"],
        'words': game["words"],
    }
    return jsonify(data)
