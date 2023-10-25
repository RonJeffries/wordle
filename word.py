class Word:
    def __init__(self, word):
        assert isinstance(word, str)
        self.word = word

    def __iter__(self):
        return iter(self.word)

    def __eq__(self, other):
        return self.word == other.word

    def __hash__(self):
        return hash(self.word)

    def __repr__(self):
        return f"Word({self.word})"

    def score(self, solution):
        # word:  abcde
        # sol:   ecbdx
        # score: 01121
        score = [0, 0, 0, 0, 0]
        sol = solution.word
        for i, c in enumerate(self.word):
            if sol[i] == c:
                score[i] = 2
            elif c in sol:
                score[i] = 1
        return score

