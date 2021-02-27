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
                       "In the beginning there was: {}",
                       "The first part of the word is important. Important that it's : {}"]
            return random.choice(options).format(self.name)
        options = ["These words seem to end with... {}.",
                   "I'd pay attention to the end of the words. Specifically: {}",
                   "OMG, ends with: {}"]
        return random.choice(options).format(self.name)