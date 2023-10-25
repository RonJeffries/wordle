from word import Word
from word_collection import WordCollection


class TestWords:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_reading_guesses(self):
        with open("valid_guesses.txt", "r") as guesses:
            lines = guesses.readlines()
        assert len(lines) == 10657

    def test_reading_solutions(self):
        with open("valid_solutions.txt", "r") as solutions:
            lines = solutions.readlines()
        assert len(lines) == 2315

    def test_word_class_exists(self):
        word = Word("abate")

    def test_drive_word_collection(self):
        w1 = Word("avast")
        w2 = Word("matey")
        words = WordCollection()
        words.append(w1)
        words.append(w2)
        assert len(words) == 2

    def test_frequency(self):
        from collections import defaultdict
        def default_value():
            return 0
        freq = defaultdict(default_value)
        letters = "aaaabbbccd"
        for c in letters:
            freq[c] += 1
        assert freq["a"] == 4
        assert freq["d"] == 1

    def test_words_from_file(self):
        wc = WordCollection.from_file("valid_solutions.txt")
        freq = wc.frequencies()
        assert freq["e"] == 1233
        counts = [(c, freq[c]) for c in freq.keys()]
        ordered = sorted(counts, key=lambda pair: pair[1], reverse=True)
        for c, f in ordered:
            print(f"{c:s}: {f:4d}")
        # assert False

    def test_words_from_big_file(self):
        wc = WordCollection.from_file("valid_guesses.txt")
        freq = wc.frequencies()
        assert freq["e"] == 5429
        counts = [(c, freq[c]) for c in freq.keys()]
        ordered = sorted(counts, key=lambda pair: pair[1], reverse=True)
        for c, f in ordered:
            print(f"{c:s}: {f:4d}")
        # assert False

    def test_known_frequencies(self):
        wc = WordCollection()
        assert isinstance(wc, WordCollection)
        for string in ["aaaabbb", "aacc"]:
            wc.append(Word(string))
        freq = wc.frequencies()
        assert freq["a"] == 6
        assert freq["b"] == 3
        assert freq["c"] == 2

    def test_score(self):
        guess = Word("abcde")
        solution = Word("ecbdx")
        score = guess.score(solution)
        assert score == [0, 1, 1, 2, 1]

    def test_has_word(self):
        guess = Word("abate")
        words = WordCollection()
        words.append(Word("tabor"))
        words.append(Word("abate"))
        assert words.has_word(guess)
        assert not words.has_word(Word("avast"))

    def test_no_solutions_in_guesses(self):
        sols = WordCollection.from_file("valid_solutions.txt")
        guesses = WordCollection.from_file("valid_guesses.txt")
        for solution_word in sols:
            assert not guesses.has_word(solution_word), f"guesses includes {solution_word}"

    def test_append_unique(self):
        sols = WordCollection.from_file("valid_solutions.txt")
        guesses = WordCollection.from_file("valid_guesses.txt")
        combined = sols.append_unique(guesses)
        assert len(combined) == len(sols) + len(guesses)

