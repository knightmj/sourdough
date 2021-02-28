from gamegen import solver
from gamegen.solver import get_local_words
from nltk.corpus import wordnet
word_helpers = None


def get_word_helpers():
    global word_helpers
    if word_helpers is None:
        word_helpers = WordHelpers()
    return word_helpers


class WordHelpers:
    words = []
    nouns = {}
    verbs = {}
    word_freq = {}
    prefixes = {}

    def __init__(self):
        self.words = set(get_local_words())
        lemmas_in_words = set(i for i in wordnet.words())
        for word in lemmas_in_words:
            if "_" not in word:
                self.words.add(word)

        self.prefixes = solver.make_lookup(self.words)
        wordnet.ensure_loaded()
        print("Loaded {} words".format(
            len(self.words)))

    def get_word_freq(self, word):
        if word in self.word_freq:
            return self.word_freq[word]
        synets = wordnet.synsets(word)
        freq = False
        for synet in synets:
            for lemma in synet.lemmas():
                freq = max(freq, lemma.count())
        self.word_freq[word] = freq
        return freq

    def is_noun(self, word):
        if word in self.nouns:
            return self.nouns[word]
        synets = wordnet.synsets(word)
        noun = False
        for synet in synets:
            noun |= synet.pos() == "n"

        self.nouns[word] = noun
        return noun

    def is_verb(self, word):
        if word in self.verbs:
            return self.verbs[word]
        synets = wordnet.synsets(word)
        verb = False
        for synet in synets:
            verb |= synet.pos() == "v"
        self.verbs[word] = verb
        return verb

