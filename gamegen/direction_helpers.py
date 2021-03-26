import random


def is_super_direction(direction):
    return abs(direction[0]) == 2 or abs(direction[1]) == 2


def direction_hint_text(directions):
    dir_list = directions

    hint = "directions: "

    # if more than 8 only print super
    if len(directions) == 8:
        dir_list = []
        for cur_direction in directions:
            if is_super_direction(cur_direction):
                dir_list.append(cur_direction)
        hint = "directions+ : "
        if len(dir_list) == 8:
            return "inside+wrap"
        if len(dir_list) == 0:
            return "inside"

    lookup = {
        (-1, 0): "E",
        (1, 0): "W",
        (0, -1): "N",
        (0, 1): "S",
        (-1, 1): "SW",
        (-1, -1): "NW",
        (1, -1): "NE",
        (1, 1): "SE",

        (-2, 0): "EE",
        (2, 0): "WW",
        (0, -2): "SS",
        (0, 2): "NN",
        (-2, 2): "SWSW",
        (-2, -2): "NWNW",
        (2, -2): "NENE",
        (2, 2): "SESE",
    }

    for direction in dir_list:
        hint += lookup[direction] + " "
    return hint


def remove_dup_directions(directions):
    """
    Remove any duplicate directions and super directions
    Args:
        directions (): list of directions to clean

    Returns:
        a list of directions without duplicates
    """
    cleaned = []
    for direction in directions:
        dup = tuple([2 * x for x in direction])
        if dup not in directions:
            cleaned.append(direction)
    return tuple(cleaned)


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
    directions = all_super_directions()
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
