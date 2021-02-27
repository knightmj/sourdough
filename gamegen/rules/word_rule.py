class WordRule:
    times_tried = 0
    times_failed = 0

    def reduce_list(self, word_list):
        self.times_tried += 1
        word_list = self.reduce_list_internal(word_list)
        if len(word_list) == 0:
            self.times_failed += 1
        return word_list

    def reduce_list_internal(self, word_list):
        pass

    def get_hint_text(self):
        pass

    def fails_ratio(self):
        if self.times_tried == 0:
            return 0
        return self.times_failed / float(self.times_tried)
