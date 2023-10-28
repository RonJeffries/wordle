from functools import reduce


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
        return not any((c in word for c in string))

    def score(self, solution):
        # word:     abcde
        # solution: ecbdx
        # score:    01121
        answer = [0, 0, 0,0, 0]
        available_letters = list(solution.word)  # cannot cache this, we destroy it
        for i, w, s in zip(range(5), self.word, solution.word):
            if w == s:
                answer[i] = 2
                available_letters[i] = 0
        for i, w in zip(range(5), self.word):
            if answer[i] != 2:
                if w in available_letters:
                    answer[i] = 1
                    available_letters[available_letters.index(w)] = 0
        return reduce(lambda product, factor: 10 * product + factor, answer)

    def score1(self, solution):
        answer = [0, 0, 0,0, 0]
        available_letters = list(solution.word)  # cannot cache this, we destroy it
        for i in range(5):
        # for i, w, s in zip(range(5), self.word, solution.word):
            if self.word[i] == solution.word[i]:
                answer[i] = 2
                available_letters[i] = 0
        for i in range(5):
        # for i, w in zip(range(5), self.word):
            if answer[i] != 2:
                if (w := self.word[i]) in available_letters:
                    answer[i] = 1
                    available_letters[available_letters.index(w)] = 0
        return answer[4] + 10*(answer[3] + 10*(answer[2] + 10*(answer[1] + 10*answer[0])))
        # return reduce(lambda product, factor: 10 * product + factor, answer)

    def to_eliminate(self, score: int):
        score_with_leading_zeros = f"{score:05}"
        keep = [c for c, s in zip(self.word, score_with_leading_zeros) if s != "0"]
        return "".join([c for c in self.word if c not in keep])

