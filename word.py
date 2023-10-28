

class Word:
    def __init__(self, word):
        assert isinstance(word, str)
        self.word = word
        self.packed = self.encode(word)

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
        answer = [0, 0, 0, 0, 0]
        guess = self.word
        soln = solution.word
        available_letters = list(soln)  # cannot cache this, we destroy it
        for i in range(5):
            if guess[i] == soln[i]:
                answer[i] = 2
                available_letters[i] = 0
        for i in range(5):
            if answer[i] != 2:
                if (w := guess[i]) in available_letters:
                    answer[i] = 1
                    available_letters[available_letters.index(w)] = 0
        return answer[4] + 10*(answer[3] + 10*(answer[2] + 10*(answer[1] + 10*answer[0])))
        # return reduce(lambda product, factor: 10 * product + factor, answer)

    def score1(self, solution):
        guess = self.word
        soln = solution.word
        # print(f"\n{guess}\n{soln}")
        available_letters = list(soln)  # cannot cache this, we destroy it
        xor = self.packed ^ solution.packed
        mask = 0xFF
        score = 0
        for i in range(5):
            if not (xor & mask):
                score = score | (0x0202020202 & mask)
                available_letters[i] = 0
            mask = mask << 8
        mask = 0xFF
        for i in range(5):
            # print(i, 4-i, guess)
            w = guess[4-i]
            # print(f"considering i {i}: {w} xor {xor:010x} mask {mask:010x} = {xor&mask:010x}")
            if xor & mask:
                if w in available_letters:
                    # print("present")
                    score = score | (0x0101010101 & mask)
                    available_letters[available_letters.index(w)] = 0
                else:
                    # print("not present")
                    pass
            else:
                # print("masked")
                pass
            mask = mask << 8
        # print(f"score {score:010x}")
        return 2002
        # return answer[4] + 10*(answer[3] + 10*(answer[2] + 10*(answer[1] + 10*answer[0])))
        # return answer[4] + 10*(answer[3] + 10*(answer[2] + 10*(answer[1] + 10*answer[0])))
        # return reduce(lambda product, factor: 10 * product + factor, answer)

    def to_eliminate(self, score: int):
        score_with_leading_zeros = f"{score:05}"
        keep = [c for c, s in zip(self.word, score_with_leading_zeros) if s != "0"]
        return "".join([c for c in self.word if c not in keep])

    @staticmethod
    def encode(string):
        code = 0
        for c in string:
            code = (code << 8) + ord(c)
        return code

    @staticmethod
    def decode(number):
        string = ""
        for i in range(5):
            string = chr(number & 0xFF) + string
            number = number >> 8
        return string

