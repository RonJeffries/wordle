import sys
import time
from functools import reduce

import pytest

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
            assert len(lines) == 10657 + 2315  # 12972

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

    def test_score_more(self):
        guess = Word("xaxax")
        solution = Word("ayyay")
        score = guess.score(solution)
        assert score == 1020

    def test_score_even_more(self):
        guess = Word("xaxax")
        solution = Word("yaayy")
        score = guess.score(solution)
        assert score == 2010

    def test_score_even_worse(self):
        guess = Word("xaxax")
        solution = Word("yyyaa")
        score = guess.score(solution)
        assert score == 1020

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

    # def test_integer_to_list_score(self):
    #     # does not work for score 1023
    #     int_score = 21023
    #     assert str(int_score) == "21023"
    #     score = [int(i) for i in str(int_score)]
    #     assert score == [2, 1, 0, 2, 3]

    def test_integer_to_list_2(self):
        int_score = 0
        string = f"00000{int_score:d}"[-5:]
        assert string == "00000"
        int_score = 12123
        string = f"00000{int_score:d}"[-5:]
        assert string == "12123"

    def test_has_word(self):
        guess = Word("abate")
        words = WordCollection()
        words.append(Word("tabor"))
        words.append(Word("abate"))
        assert words.has_word(guess)
        assert not words.has_word(Word("avast"))

    # test is slow and generally useless
    # def test_no_solutions_in_guesses(self):
    #     sols = WordCollection.from_file("valid_solutions.txt")
    #     guesses = WordCollection.from_file("valid_guesses.txt")
    #     for solution_word in sols:
    #         assert not guesses.has_word(solution_word), f"guesses includes {solution_word}"

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

    def test_leading_zero(self):
        n = 0
        assert f"{n:05}" == "00000"
        n = 123
        assert f"{n:05}" == "00123"
        n = 20123
        assert f"{n:05}" == "20123"

    # @pytest.mark.skip("abc faster than list")
    # def test_in_speed(self):
    #     n = 10000000
    #     r0 = time.time()
    #     for i in range(n):
    #         pass
    #     r1 = time.time()
    #     raw = r1 - r0
    #     string_time_0 = time.time()
    #     for i in range(n):
    #         t = "z" in "abc"
    #     string_time_1 = time.time()
    #     string_time = string_time_1 - string_time_0 - raw
    #     list_time_0 = time.time()
    #     for i in range(n):
    #         t = "z" in ["a", "b", "c"]
    #     list_time_1 = time.time()
    #     list_time = list_time_1 - list_time_0 - raw
    #     assert string_time*3 < list_time

    def test_to_eliminate(self):
        word = Word("abcde")
        score = 1020
        assert word.to_eliminate(score) == "ace"

    # @pytest.mark.skip("about 30 seconds to run")
    # def test_combined_x_solutions(self):
    #     sols = WordCollection.from_file("valid_solutions.txt")
    #     guesses = WordCollection.from_file("valid_guesses.txt")
    #     t0 = time.time()
    #     guess_count = 0
    #     sol_count = 0
    #     for guess in guesses.words:
    #         guess_count += 1
    #         for sol in sols.words:
    #             score = guess.score(sol)
    #             sol_count += 1
    #     t1 = time.time()
    #     print(t1 - t0)
    #     assert guess_count == len(guesses)
    #     assert sol_count == len(guesses) * len(sols)
    #     assert False

    # @pytest.mark.skip("about 0.4 seconds to run")
    # def test_nested_loops(self):
    #     sols = WordCollection.from_file("valid_solutions.txt")
    #     guesses = WordCollection.from_file("valid_guesses.txt")
    #     t0 = time.time()
    #     guess_count = 0
    #     sol_count = 0
    #     for guess in guesses.words:
    #         guess_count += 1
    #         for sol in sols.words:
    #             sol_count += 1
    #     t1 = time.time()
    #     assert guess_count == len(guesses)
    #     assert sol_count == len(guesses) * len(sols)
    #     assert t1 - t0 < 0.5

    # @pytest.mark.skip("about 1.2 seconds per million")
    # def test_score_speed(self):
    #     w1 = Word("abcde")
    #     w2 = Word("edcba")
    #     assert w1.score(w2) == 11211
    #     n = 1000000
    #     t0 = time.time()
    #     for i in range(n):
    #         t = w1.score(w2)
    #     t1 = time.time()
    #     assert t1 - t0 < 1.5

    def test_compare_score(self):
        sols = WordCollection.from_file("valid_solutions.txt")
        guesses = WordCollection.from_file("valid_guesses.txt")
        guess = Word("crate")
        solution = Word("prone")
        assert guess.score1(solution) == guess.score(solution)
        n = 100000
        loop_0 = time.time()
        for i in range(n):
            pass
        loop_delta = time.time() - loop_0
        current_0 = time.time()
        for i in range(n):
            sc = guess.score(solution)
        current_delta = round(time.time() - current_0 - loop_delta, 3)
        new_0 = time.time()
        for i in range(n):
            sc = guess.score1(solution)
        new_delta = round(time.time() - new_0 - loop_delta, 3)
        print(current_delta, new_delta)
        print(f"\nscore1 {new_delta:.3f}, score {current_delta:.3f} = {current_delta / new_delta:.3f}")
        assert False

    def test_encode_decode(self):
        # for i in range(5):
        #     print(f"{(0x1F << (5*i)):x}")
        assert Word.decode(Word.encode("zebra")) == "zebra"
        zebra = Word("zebra")
        zelda = Word("zelda")
        xor = zebra.packed ^ zelda.packed
        print(f"\n{zebra.packed:010x}")
        print(f"{xor:010x}")
        assert xor == 0xe1600



