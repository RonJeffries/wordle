class Word:
    def __init__(self, word):
        assert isinstance(word, str)
        self.word = word
        self._optimize_score = [0, 0, 0, 0, 0]
        # saved so we never reallocate the list

    def __iter__(self):
        return iter(self.word)

    def __eq__(self, other):
        return self.word == other.word

    def __hash__(self):
        return hash(self.word)

    def __repr__(self):
        return f"Word({self.word})"

    def contains_none(self, string):
        word = self.word
        return all((c not in word for c in string))

    def score(self, solution):
        # word:  abcde
        # sol:   ecbdx
        # score: 01121
        score = self._optimize_score
        sol = list(solution.word)  # cannot cache this, we destroy it
        for i, c in enumerate(self.word):
            if c in sol:
                if sol[i] == c:
                    score[i] = 2
                    sol[i] = 0
                else:
                    score[i] = 1
                    sol[sol.index(c)] = 0
            else:
                score[i] = 0
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

