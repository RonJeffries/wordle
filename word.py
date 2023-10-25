class Word:
    def __init__(self, word):
        self.word = word

    def __iter__(self):
        return iter(self.word)
