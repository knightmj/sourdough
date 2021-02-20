from collections import defaultdict
from datetime import datetime
import random


def n_random_directions(n):
    """
    Return a list of random cardinal directions
    Args:
        n (): now may directions to return

    Returns:
        a list of tuples
    """
    directions = all_cardinal_directions()
    return tuple(random.sample(directions, n))


def n_super_directions(n):
    """
    return a list of N random super directions
    Args:
        n (): how may directions to provide
    Returns:
        a list of tuples
    """
    directions = all_cardinal_directions()
    return tuple(random.sample(directions, n))


def all_super_directions():
    """
    Get all directions to wrap around edges. Note super directions
    are redundant to their non super counterpart.  Meaning (-2,0)
    will wrap around and it will also move (-1,0) inside of the grid.

    Returns:
        8 super directions
    """
    return (
        (-2, -2), (-2, 0), (-2, 2),
        (0, -2), (0, 2),
        (2, -2), (2, 0), (2, 2),
    )


def all_cardinal_directions():
    """
    Get all basic cardinal directions except staying in the same place
    Returns:

    """
    return (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1),
    )


def make_graph(grid, directions):
    """
    Make a graph from this grid of letter strings
    Args:
        grid (): a list of N strings all of the same length
        directions (): cardinal directions or super directions to be used in
        creating child nodes

    Returns:
        the graph and a character dictionary (keys are tuples, values are character)
        for the graph
    """
    root = None
    graph = {root: set()}
    character_dict = {root: ''}

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            character_dict[(i, j)] = char
            node = (i, j)
            children = set()
            graph[node] = children
            graph[root].add(node)
            add_children(node, children, grid, directions)

    return graph, character_dict


def constrain_circular(v, min_value, max_value):
    """
    Return a circular list wrapping for the provided value v, if it's before
    or after the min or max reflect it to the other side of the list
    Args:
        v (): value to check for wrapping
        min_value (): min list index
        max_value (): max list index

    Returns:
        a wrapped index
    """
    if v < min_value:
        return max_value + v + min_value
    else:
        if v > max_value - 1:
            return max_value - v + min_value
    return v


def check_and_add_child(x, y, x_max, y_max, children, x_min=0, y_min=0):
    """
    if these x and y values are inside of the grid 0, maxes add
    them to the list of children. Otherwise fail silently
    Args:

        x (): x value to add
        y (): y value to add
        x_max (): max x value
        y_max (): max y value
        children (): list of children to add (x,y) to
        y_min (): min y value
        x_min (): min x value

    Returns:
        Nothing
    """
    if not (x_min <= x < x_max):
        return
    if not (y_min <= y < y_max):
        return
    children.add((x, y))


def get_offset_form_super(value):
    """
    A super direction is coded as (-2,0) to imply that
    we want to go (-1,0) and wrap around. So the offset
    will just be turning the 2s into 1s.
    Args:
        value (): super value to change

    Returns:
        A -1,0, or 1 offset
    """
    if value == 0:
        return 0
    if value == -2:
        return -1
    return 1


def add_children(node, children, grid, directions=all_cardinal_directions()):
    """
    Follow the provided directions from this node on the grid and create a list
    of children
    Args:
        node (): A tuple of the x,y position of this node
        children (): a list of tuples of children
        grid (): the grid we will walk
        directions (): a list of directions we can move

    Returns:
        Nothing
    """
    x0, y0 = node
    x_max = len(grid)
    y_max = len(grid[0])
    for direction in directions:

        if abs(direction[0]) > 1 or abs(direction[1]) > 1:
            # this is a super direction, it means go one space in that
            # direction even if it wraps around the board. super directions
            # are redundant to their non-super counterparts so (-1,0) is not
            # needed of (-2,0) is provided.
            x_offset = get_offset_form_super(direction[0])
            y_offset = get_offset_form_super(direction[1])
            x = x0 + x_offset
            y = y0 + y_offset
            x = constrain_circular(x, 0, x_max)
            y = constrain_circular(y, 0, y_max)

            check_and_add_child(x, y, x_max, y_max, children)
        else:
            # this is a non-super direction, bounds check it and move on
            if direction[0] == 0 and direction[1] == 0:
                continue
            x = x0 + direction[0]
            y = y0 + direction[1]
            check_and_add_child(x, y, x_max, y_max, children)


def to_word(character_dictionary, pos_list):
    """
    Convert a list of points into a list of words with
    a point list and a point to letter lookup
    Args:
        character_dictionary (): a tuple to character lookup
        pos_list (): a list of tuples of points in the lookup

    Returns:
        a string of the letters from the position list
    """
    return ''.join(character_dictionary[x] for x in pos_list)


def find_words(graph, character_dictionary, position, prefix, results, words, prefixes):
    """
    Recurse the graph and look for valid words.
    Args:
        graph ():  mapping (x,y) to set of reachable positions
        character_dictionary (): mapping (x,y) to character
        position ():  current position (x,y) -- equals prefix[-1]
        prefix (): list of positions in current string
        results (): set of words found
        words (): set of valid words in the dictionary
        prefixes ():  set of valid words or prefixes thereof

    Returns:
        Nothing, results are placed in the result list
    """
    word = to_word(character_dictionary, prefix)

    if word not in prefixes:
        return

    if word in words:
        results.add(word)

    for child in graph[position]:
        if child not in prefix:
            find_words(graph, character_dictionary, child, prefix + [child], results, words, prefixes)


def get_words(input_file, norm=None):
    """
    Get the words from a file, normalize with this method if provided
    Args:
        input_file (): filename of file to read words from
        norm ():  a function that can be run to normalize the word

    Returns:
        a list of words
    """
    word_list = []
    with open(input_file, "r") as f:
        for file_line in f:
            if norm:
                file_line = norm(file_line)
            word_list.append(file_line)

    return word_list


def normalize(s):
    """
    Normalize the provided string
    Args:
        s (): string to normalize

    Returns:

    """
    return s.strip().lower()


def get_local_words():
    """
    Load words from /usr/share/dict/words and normalize them

    Returns:
        A list of words including proper nouns
    """
    return get_words("/usr/share/dict/words", norm=normalize)


def make_lookup(world_list):
    """
    Convert each word in the word list into a set of prefixes
    Args:
        world_list ():
    Returns:
        A set of all possible prefixes for the words in the word list

    """
    prefixes = set()
    for w in world_list:
        for i in range(len(w) + 1):
            prefixes.add(w[:i])

    return prefixes


def solve_board(board, word_list=get_local_words(), directions=all_cardinal_directions()):
    """
    Find all words in the provided letter board that meet the directional constraints
    are that are in the word list
    Args:
        board (): A list of strings all of the same length
        word_list (): a list of words to find
        directions (): a list of directions or super directions to move in the grid

    Returns:
        A list of valid words from the word list in the board
    """
    graph, character_dict = make_graph(board, directions)
    prefixes = make_lookup(word_list)
    results = set()
    find_words(graph, character_dict, None, [], results, word_list, prefixes)
    return results


def exercise_board(board, **kwargs):
    """
    Run the solve function on the provided board and report times
    Args:
        board (): board to solve
        **kwargs (): any needed args to pass to the solve method

    Returns:
        Nothing
    """
    start = datetime.now()
    words = solve_board(board, **kwargs)
    elapsed = datetime.now() - start
    print("found ", len(words), "words", elapsed)


def get_test_board():
    return ["asletm",
            "gtrtsn",
            "bsowlo",
            "milkep",
            "oilkeq",
            "blowlo"]


def exercise_board_simple():
    exercise_board(get_test_board())


def exercise_board_word_list():
    exercise_board(get_test_board(), word_list=["asle", "agb", "miow", "blse"])


def exercise_board_directions():
    exercise_board(get_test_board(), directions=n_random_directions(3))


def exercise_board_super_directions():
    exercise_board(get_test_board(), directions=all_super_directions())


def exercise_board_super_directions_word_list():
    exercise_board(get_test_board(), word_list=["asle", "agb", "miow", "blse"], directions=all_super_directions())


def exercise_boards():
    exercise_board_simple()
    exercise_board_word_list()
    exercise_board_directions()
    exercise_board_super_directions()
    exercise_board_super_directions_word_list()


if __name__ == "__main__":
    exercise_boards()
