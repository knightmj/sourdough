import json
import math

from gamegen import solver
from gamegen.direction_helpers import is_super_direction, direction_hint_text
from gamegen.words import get_word_helpers


class GameBoard:
    board = []
    rules = []
    valid_words = set()
    words = []
    directions = []
    goal_words = 0
    difficulty = 0.0
    uniqueness = 0.0
    time = 0.0
    goal_word_percent = .66

    def __init__(self, directions_in, board_in, rules_in, goal_word_percent):
        self.board = board_in
        self.rules = rules_in
        self.directions = directions_in
        self.goal_word_percent = goal_word_percent

    def solve_and_apply_rules(self):
        helpers = get_word_helpers()

        self.words = solver.solve_board(self.board,
                                        directions=self.directions,
                                        word_list=helpers.words,
                                        prefixes=helpers.prefixes)
        if len(self.words) == 0:
            return

        self.valid_words = set(self.words)

        pointless = []
        for rule in self.rules:
            start_len = len(self.valid_words)
            self.valid_words = rule.reduce_list(self.valid_words)
            if start_len == len(self.valid_words):
                pointless.append(rule)

        # remove any rules that did not change the valid list
        self.rules = [rule for rule in self.rules if rule not in pointless]

        self.valid_words = set(self.valid_words)
        for word in self.valid_words:
            word_frequency = helpers.get_word_freq(word)
            if word_frequency > 0:
                self.goal_words += 1

        self.goal_words = math.floor(self.goal_word_percent * self.goal_words)

        self.time = self.goal_words * 90 * self.goal_word_percent

    def is_healthy(self):
        # not many good words found, so skip this one
        if 5 > self.goal_words:
            return False
        return True

    def set_difficulty_uniqueness(self):
        direction_score = 0
        for direction in self.directions:
            if is_super_direction(direction):
                direction_score += 3
            else:
                direction_score += 1
        rule_sore = len(self.rules) * 20
        extra_words = len(self.valid_words) - self.goal_words
        number_words = len(self.valid_words)
        filtered_words = len(self.words) - len(self.valid_words)
        goal_percent = self.goal_word_percent * 100

        self.difficulty = direction_score + rule_sore + \
                          (number_words / 2.0) + (extra_words / 2.0) + self.goal_words + \
                          (filtered_words / 2.0) + (goal_percent * 10)

        for rule in self.rules:
            # the more this rule has failed the more unique we become
            self.uniqueness += rule.fails_ratio()

    def hint_text(self):
        rule_hint = ""
        for rule in self.rules:
            rule_hint += rule.get_hint_text() + " -- "

        return direction_hint_text(self.directions) + " -- " + rule_hint

    def two_d_bord(self):
        board_2d = []
        for row in self.board:
            board_2d.append(list(row.upper()))
        return board_2d

    def to_json(self):
        return json.dumps({
            "board": self.two_d_bord(),
            "valid": list(self.valid_words),
            "invalid": list(self.words - self.valid_words),
            "rule_text": self.hint_text(),
            "time_s": self.time,
            "text_fully_revealed_at_s": 90,
            "number_of_words": self.goal_words,
            "uniqueness": self.uniqueness,
            "difficulty": self.difficulty,
        }, indent=2, ensure_ascii=False)

    def ratio(self):
        return len(self.valid_words) / float(len(self.words))

    def __eq__(self, other):
        return self.difficulty == other.difficulty

    def __lt__(self, other):
        return self.difficulty < other.difficulty
