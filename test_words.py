import sys
from functools import reduce

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

    def test_reading_combined(self):
        with open("valid_combined.txt", "r") as combined:
            lines = combined.readlines()
            assert len(lines) == 10657 + 2315

    def test_memory_size(self):
        combo = WordCollection.from_file("valid_combined.txt")
        size = sys.getsizeof(combo)
        assert size < 100
        words = combo.words
        words_size = sys.getsizeof(words)
        assert words_size < 120000

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
        # for c, f in ordered:
            # print(f"{c:s}: {f:4d}")
        # assert False

    def test_words_from_big_file(self):
        wc = WordCollection.from_file("valid_guesses.txt")
        freq = wc.frequencies()
        assert freq["e"] == 5429
        counts = [(c, freq[c]) for c in freq.keys()]
        ordered = sorted(counts, key=lambda pair: pair[1], reverse=True)
        # for c, f in ordered:
            # print(f"{c:s}: {f:4d}")
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
        assert score == 1121
        score_again = guess.score(solution)
        assert score_again == 1121

    def test_score_caching(self):
        guess = Word("abcde")
        solution = Word("ecbdx")
        score_1 = guess.score(solution)
        assert score_1 == 1121
        score_2 = guess.score(solution)
        assert score_1 == 1121, "fails, cached?"
        assert score_2 == 1121
        # assert score_1 == score_2, "cannot cache solution list"

    def test_list_score_to_integer(self):
        score = [2, 1, 0, 2, 3]
        int_score = 0
        for s in score:
            int_score = 10*int_score + s
        assert int_score == 21023

    def test_list_score_to_int_reduce(self):
        score = [2, 1, 0, 2, 3]
        int_score = reduce(lambda product, factor: 10*product+factor, score)
        assert int_score == 21023

    def test_integer_to_list_score(self):
        int_score = 21023
        assert str(int_score) == "21023"
        score = [int(i) for i in str(int_score)]
        assert score == [2, 1, 0, 2, 3]

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

    def test_strict_score(self):
        g = Word("aaxxx")
        s = Word("abcde")
        score = g.score(s)
        assert score == 20000

    def test_strict_score_2(self):
        g = Word("aaxxx")
        s = Word("zzzza")
        score = g.score(s)
        assert score == 10000

    def test_exact_after_removal(self):
        g = Word("azczx")
        s = Word("axcxq")
        score = g.score(s)
        assert score == 20201


