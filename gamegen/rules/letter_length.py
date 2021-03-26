import random

from gamegen.rules.word_rule import WordRule


class LetterLengthRule(WordRule):
    min = 0
    max = 0

    def __init__(self, min_len, max_len):
        self.min = min_len
        self.max = max_len

    def reduce_list_internal(self, word_list):
        reduced = []
        for word in word_list:
            real_max = self.max
            # if we don't want a max it will be -1
            if real_max == -1:
                real_max = len(word) + 1

            if self.min <= len(word) <= self.max:
                reduced.append(word)
        return reduced

    def get_hint_text(self):
        if self.min == 0:
            options = ["Your words my be not longer than dis many fingers: {}.",
                       "Words with at least {} letters.",
                       "At least {} of da letters."]
            return random.choice(options).format(self.max)
        if self.max == -1:
            options = ["Yo words my gonna need ta be longer than dis: {}",
                       "It can't get any betters than words with at least {} letters.",
                       "At least {} many letters, so little time."]
            return random.choice(options).format(self.min)
        if self.min == self.max:
            options = ["Exactamundo {}",
                       "Maka dem all the same siza: {}",
                       "No more no less than the best which is {}."]
            return random.choice(options).format(self.min)

        options = ["From {}-{} letters.",
                   "{}-{} letters.",
                   "{}-{} many letters, so little time."]
        return random.choice(options).format(self.min, self.max)