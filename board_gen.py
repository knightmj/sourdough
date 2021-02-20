from datetime import datetime

from gamegen import solver
import random


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


def make_board(letters, x,y):
    board = []
    for i in range(0, y):
        board.append(
            "".join(random.sample(letters, x))
        )
    return board


if __name__ == "__main__":
    board = make_board(word_game_dist(), 10, 10)
    start = datetime.now()
    words = solver.solve_board(board, directions=solver.all_super_directions())
    for word in board:
        print(word)
    print("found", len(words), "words", datetime.now() - start)