import random

from gamegen.rules.word_rule import WordRule


class SubstringRule(WordRule):
    substring = ""
    substring2 = ""

    def __init__(self, needle, second_needle=None):
        self.substring = needle
        self.substring2 = second_needle

    def reduce_list_internal(self, word_list):
        reduced = []
        for word in word_list:
            first = self.substring in word
            second = self.substring2 is None or self.substring2 in word
            # do we just have 1 string to check
            if self.substring2 is None:
                if first:
                    reduced.append(word)
            # are we checking both strings are in there
            elif first and second:
                reduced.append(word)

        return reduced

    def get_hint_text(self):
        options = ["Words need to represent with : {}.",
                   "What's in dem words. Is it: {}. Yeah it is.",
                   "All these words have something in common. I think {}. sry typo"]
        term = self.substring
        if self.substring2 is not None:
            term = self.substring + " and " + self.substring2

        return random.choice(options).format(term)
