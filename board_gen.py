import sys
import time

from gamegen import solver
from gamegen.direction_helpers import *
import random
import os

from gamegen.game_board import GameBoard
from gamegen.rules.pass_test_rule import PassesTestRule
from gamegen.rules.letter_length import LetterLengthRule
from gamegen.rules.starts_ends_rule import StarsEndsRule
from gamegen.rules.substring import SubstringRule

from gamegen.words import get_word_helpers


def word_game_dist():
    dist = [
        ['A', 9], ['B', 2], ['C', 2], ['D', 4], ['E', 12],
        ['F', 2], ['G', 3], ['H', 2], ['I', 9], ['J', 1],
        ['K', 1], ['L', 4], ['M', 2], ['N', 6], ['O', 8],
        ['P', 2], ['Q', 1], ['R', 6], ['S', 4], ['T', 6],
        ['U', 4], ['V', 2], ['W', 2], ['X', 1], ['Y', 2],
        ['Z', 1]]
    letters = ""
    for pair in dist:
        letters += pair[0] * pair[1]
    return letters.lower()


def make_board(letters, x, y):
    board = []
    for i in range(0, y):
        board.append(
            "".join(random.sample(letters, x))
        )
    return board


def get_word_board(w, h):
    helpers = get_word_helpers()
    return random.sample(helpers.hist[w], h)


def get_random_board_patten():
    pattens = [
        [
            "      *       ",
            "     ***      ",
            "    ******    ",
            "  **********  ",
            "**************",
            "     ***      ",
        ],
        [
            "  ***   ***  ",
            "****** ******",
            " *********** ",
            "  *********  ",
            "   ******    ",
            "     **      ",
        ],
        [
            "  *******  ",
            " ********* ",
            "***     ***",
            "***     ***",
            "***     ***",
            " ********* ",
            "  *******  ",
        ],
        [
            "***         ",
            "*****       ",
            "*******     ",
            "*********   ",
            "************",
        ],
        [
            "      *       ",
            "     ***      ",
            "    ******    ",
            "  **********  ",
            "**************",
        ],
        [
            "***    ",
            "***    ",
            "***    ",
            "***    ",
            "*******",
            "*******",
        ],
        [
            "*** ****",
            "*** ****",
            "*** ****",
            "*** ****",
            "*** ****",
            "*** ****",
        ],
        [
            "****** *",
            "***** **",
            "**** ***",
            "*** ****",
            "** *****",
            "* ******",
        ],
        [
            "******    ******",
            "*** ***  *** ***",
            "***  ******  ***",
            "***    **    ***",
            "***          ***",
        ],
    ]
    return random.choice(pattens)


def patten_board(patten):
    height = len(patten)
    width = len(patten[0])
    b = []
    for y in range(0, height):
        b.append(list(" " * width))

    letters = word_game_dist()

    for col in range(0, width):
        for row in range(0, height):
            if patten[row][col] == "*":
                b[row][col] = random.choice(letters)

    final_board = []
    for y in range(0, height):
        final_board.append("".join(b[y]))

    return final_board


def get_substring_rules():
    rules = []
    terms = ["e", "el", "et", "i", "ee", "oo", "r", "s", "t", "z"]
    for substring in terms:
        rule = SubstringRule(substring)
        rules.append(rule)
    for substring in terms:
        for substring2 in terms:
            if substring2 == substring:
                continue
            rule = SubstringRule(substring, substring2)
            rules.append(rule)

    return rules


def get_start_end():
    position = [True, False]
    terms = {"vowels": list("aeiouy"),
             "consonants": list("bcdfghjklmnpqrstvwxyz"),
             "frog": list("frog"),
             "potato": list("potato"),
             "wedding": list("wedding"),
             "minos": list("minos"),
             "mike": list("mike"),
             "lisa": list("lisa")}

    rules = []
    for start in position:
        for name, letters in terms.items():
            rule = StarsEndsRule(start, letters, name)
            rules.append(rule)
    return rules


def get_words_in():
    word_helpers = get_word_helpers()
    return [PassesTestRule(word_helpers.is_noun, "nouns"),
            PassesTestRule(word_helpers.is_verb, "verbs")]


def get_letter_length():
    rules = []
    for min_len in [0, 4, 5, 6]:
        for max_len in [-1, 3, 4, 5]:
            if min_len > max_len:
                continue
            rule = LetterLengthRule(min_len, max_len)
            # print(rule.get_hint_text())
            rules.append(rule)
    return rules


def get_word_rules():
    rules = {"letter_len": get_letter_length(),
             "substring": get_substring_rules(),
             "starts_ends": get_start_end(),
             "words_in": get_words_in()}
    return rules


def board_sizes():
    one_dimensions = [1, 2, 3, 4, 6, 7, 8, 9]
    sizes = []
    for x in one_dimensions:
        for y in one_dimensions:
            if x * y > 6:
                if (y, x) not in sizes:
                    sizes.append((x, y))
    return sizes


def setup_rules():
    word_rules = get_word_rules()
    for key, rules in word_rules.items():
        print("rule group:", key, "rules:", len(rules))
    return word_rules


def generate_board(size):
    if random.randint(0, 5) == 1:
        board = patten_board(get_random_board_patten())
    elif size[0] > 2 and random.randint(0, 5) == 1:
        board = get_word_board(size[0], size[1])
    else:
        board = make_board(word_game_dist(), size[0], size[1])
    return board


def print_status(batch_start, boards_made, games, total):
    print("\ngames so far:", len(games))
    print("games tried:", boards_made)
    print("total to try:", total)
    if batch_start:
        elapsed = (time.time() - batch_start) / boards_made
        print("seconds left:", (total - boards_made) * elapsed)
    else:
        batch_start = time.time()
    print("progress:", round(boards_made / float(total) * 100, 2))
    sys.stdout.flush()


def get_directions(all_directions, directions, super_directions):
    for direction_count in directions:
        for super_direction_count in super_directions:
            directions = simplify_directions(direction_count, super_direction_count)
            all_directions.append(directions)
    all_directions.append([(0, 1)])  # right only
    all_directions.append([(-1, 0)])  # down only
    all_directions.append([(0, -1), (0, 1)])  # left right only
    all_directions.append([(-1, 0), (1, 0)])  # up/down only
    all_directions.append([(-1, 0), (1, 0), (0, -1), (0, 1)])  # left right up down


def select_rules(word_rules):
    rules = []
    for _, cur_rules in word_rules.items():
        if random.randint(0, 1) == 0:
            rules.append(random.choice(cur_rules))
    return rules


def simplify_directions(direction_count, super_direction_count):
    directions = n_random_directions(direction_count)
    super_directions = n_super_directions(super_direction_count)
    if super_direction_count > 0:
        all_dirs = directions + super_directions
        directions = remove_dup_directions(all_dirs)
    return directions


def save_output(games, folder, start_index):
    cnt = start_index
    with open("boards_" + str(len(games)) + ".csv", "w") as f:
        f.write("id, difficulty,uniqueness,rules,goal words,valid words,total words, cells, hint\n")
        for game in games:
            csv = ",".join([str(cnt), str(game.difficulty), str(game.uniqueness), str(len(game.rules)),
                            str(game.goal_words), str(len(game.valid_words)), str(len(game.words)),
                            str(len(game.board) * len(game.board[0])),
                            game.hint_text()])
            f.write(csv + "\n")
            with open(
                    os.path.join(folder,
                                 str(cnt) + ".json"), "w") as board_file:
                board_file.write(game.to_json())
            cnt += 1
            sys.stdout.flush()


def generate(folder, batch):
    # setup loop vars
    games = []
    boards_made = 0
    directions = [8]  # all directions
    super_directions = [0, 8]  # none or all super directions
    max_tries = 50
    sizes = board_sizes()
    percents = [.4, .6, .8, .9]
    all_directions = []

    word_rules = setup_rules()
    get_directions(all_directions, directions, super_directions)

    total = len(all_directions) * max_tries * len(sizes)
    batch_start = None

    for directions in all_directions:
        for size in sizes:
            print_status(batch_start, boards_made, games, total)
            for i in range(0, max_tries):
                board = generate_board(size)
                boards_made += 1
                rules = select_rules(word_rules)
                game = GameBoard(directions, board, rules,
                                 random.choice(percents))
                game.solve_and_apply_rules()
                if game.is_healthy():
                    games.append(game)
    for game in games:
        game.set_difficulty_uniqueness()
    games.sort()
    save_output(games, folder, (batch * total) + 1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("board_gen.py <output> <batch>")
        exit()

    # load up the words
    print("loading dictionary")
    helpers = get_word_helpers()
    print("making boards")
    if not os.path.exists(sys.argv[1]):
        os.mkdir(sys.argv[1])

    generate(sys.argv[1], int(sys.argv[2]))
