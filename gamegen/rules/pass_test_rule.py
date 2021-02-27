import random

from gamegen.rules.word_rule import WordRule


class PassesTestRule(WordRule):
    test = set()
    name = ""

    def __init__(self, word_test, friendly_name):
        self.test = word_test
        self.name = friendly_name

    def reduce_list_internal(self, word_list):
        reduced = []
        for word in word_list:
            if self.test(word):
                reduced.append(word)
        return reduced

    def get_hint_text(self):
        options = ["These words are all: {}.",
                   "I'd pay attention to the kind of the words there are. Specifically: {}",
                   "OMG,these are: {}"]
        return random.choice(options).format(self.name)
