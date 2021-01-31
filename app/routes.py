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

    resp = make_response(render_template('play.html', user=user,
                                         board=game['level']['board'],
                                         game=game,
                                         players=game["players"].keys()))
    if set_cookie:
        resp.set_cookie('user_uid', user_id)
        resp.set_cookie('user_name', name)
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
    text = game["level"]["rule_text"][:letters] + extra * "*"

    data = {
        'players': [],
        'remaining_words': remaining_words,
        'remaining_time': remaining_time,
        'rule_text': text,
        'words': game["words"],
    }
    return jsonify(data)
