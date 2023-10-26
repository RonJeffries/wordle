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

    def contains_none(self, string):
        my_string = self.word
        for c in string:
            if c in my_string:
                return False
        return True

    def score(self, solution):
        # word:  abcde
        # sol:   ecbdx
        # score: 01121
        score = [0, 0, 0, 0, 0]
        sol = list(solution.word)
        for i, c in enumerate(self.word):
            if sol[i] == c:
                score[i] = 2
                sol[i] = 0
            elif c in sol:
                score[i] = 1
                sol[sol.index(c)] = 0
        return score

    def to_eliminate(self, score):
        keep = ""
        for i, s in enumerate(score):
            if s:
                keep += self.word[i]
        result = ""
        for c in self.word:
            if c not in keep:
                result += c
        return result

