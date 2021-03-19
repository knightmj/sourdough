import random

from gamegen.rules.word_rule import WordRule


class StarsEndsRule(WordRule):
    start = False
    chars = []
    name = ""

    def __init__(self, starts_with, char_list, friendly_name):
        self.start = starts_with
        self.chars = char_list
        self.name = friendly_name

    def reduce_list_internal(self, word_list):
        reduced = []
        for word in word_list:
            if self.start:
                if word[0] in self.chars:
                    reduced.append(word)
            elif word[-1] in self.chars:
                reduced.append(word)

        return reduced

    def get_hint_text(self):
        if self.start:
            options = ["These words seem to start with... {}.",
                       "In the beginning was one of these letters: {}",
                       "The first part of the word is important. Is one of : {}"]
            return random.choice(options).format(self.name)
        options = ["These words seem to end with the letters... {}.",
                   "Ends with a letter from {}",
                   "OMG, ends with a letter from: {}"]
        return random.choice(options).format(self.name)