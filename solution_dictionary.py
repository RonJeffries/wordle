from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from math import ceil, log2

from score_description import ScoreDescription
from word_collection import WordCollection


class Statistic:
    def __init__(self, word, number_of_buckets, max_words, min_words, avg_words, expected_info):
        self.word = word
        self.number_of_buckets = number_of_buckets
        self.max_words = max_words
        self.min_words = min_words
        self.avg_words = avg_words
        self.expected_info = expected_info

    def __repr__(self):
        return (f"{self.word.word} {self.expected_info:5.2f} {self.number_of_buckets:4d} {self.min_words:5d} "
                f"{self.avg_words:7.2f}{self.max_words:5d}")

    @classmethod
    @property
    def header(cls):
        return "\nWord  Info  Buckets Min   Avg   Max"


class GuessDescription:
    def __init__(self, guess_word, solutions):
        self.guess_word = guess_word
        self.score_descriptions = {}
        self.solutions_count = len(solutions)
        for solution in solutions:
            score = guess_word.score(solution)
            self.classify_word(score, solution)

    def __repr__(self):
        return f"GD({self.guess_word.word}:\n  {self.score_descriptions}"

    def classify_word(self, score, solution):
        try:
            description = self.score_descriptions[score]
        except KeyError:
            description = ScoreDescription(score)
            self.score_descriptions[score] = description
        description.add_word(solution)

    def expected_information(self):
        total = 0
        for score_description in self.score_descriptions.values():
            probability = score_description.probability(self.solutions_count)
            log = log2(1/probability)
            total += probability*log
        return total


    @property
    def buckets(self):
        return self.score_descriptions.values()

    @property
    def number_of_buckets(self):
        return len(self.score_descriptions)

    def solutions_for(self, score):
        try:
            return self.score_descriptions[score]
        except KeyError:
            return ScoreDescription(score)


class SolutionDictionary:
    def __init__(self, guesses: WordCollection, solutions: WordCollection):
        assert isinstance(guesses, WordCollection)
        assert isinstance(solutions, WordCollection)
        self.dict = {}
        self.merge_dict(guesses, solutions)

    def __repr__(self):
        return f"SD{self.dict}"

    @classmethod
    def from_slices(cls, solutions, *guess_slices):
        none = WordCollection()
        instance = cls(none, none)
        for guesses in guess_slices:
            instance.merge_dict(guesses, solutions)
        return instance

    def merge_dict(self, guesses, solutions):
        guess_descriptions = map(self.guess_description, guesses, repeat(solutions))
        for description in guess_descriptions:
            self.dict[description.guess_word] = description

    def append(self, other_solution_dictionary):
        for k,v in other_solution_dictionary.dict.items():
            self.dict[k] = v

    def guess_description(self, guess, solutions):
        return GuessDescription(guess, solutions)

    def create_statistics(self):
        stats = []
        for word in self.dict:
            guess_description = self.dict[word]  # {score -> scoredWords}
            expected_info = guess_description.expected_information()
            number_of_buckets = guess_description.number_of_buckets
            max_words = max(len(bucket) for bucket in guess_description.buckets)
            min_words = min(len(bucket) for bucket in guess_description.buckets)
            avg_words = sum(len(bucket) for bucket in guess_description.buckets) / number_of_buckets
            stat = Statistic(word, number_of_buckets, max_words, min_words, avg_words, expected_info)
            stats.append(stat)

        def my_key(stat: Statistic):
            return stat.expected_info

        stats.sort(key=my_key, reverse=True)
        return stats

    def solutions_for(self, guess, score):
        guess_description = self.dict[guess]
        return guess_description.solutions_for(score)
