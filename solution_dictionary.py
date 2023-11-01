from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from math import ceil

from score_description import ScoreDescription
from word_collection import WordCollection


class Statistic:
    def __init__(self, word, number_of_buckets, max_words, min_words, avg_words):
        self.word = word
        self.number_of_buckets = number_of_buckets
        self.max_words = max_words
        self.min_words = min_words
        self.avg_words = avg_words

    def __repr__(self):
        return (f"{self.word.word} {self.number_of_buckets:4d} {self.min_words:5d} "
                f"{self.avg_words:7.2f}{self.max_words:5d}")

    @classmethod
    @property
    def header(cls):
        return "\nWord  Buckets Min   Avg   Max"


class GuessDescription:
    def __init__(self, guess_word, solutions):
        self.guess_word = guess_word
        self.score_descriptions = {}
        for solution in solutions:
            score = guess_word.score(solution)
            self.classify_word(score, solution)

    def classify_word(self, score, solution):
        try:
            description = self.score_descriptions[score]
        except KeyError:
            description = ScoreDescription(score)
            self.score_descriptions[score] = description
        description.add_word(solution)

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
        self.dict = self.create_dict(guesses, solutions)

    def append(self, other_solution_dictionary):
        for k,v in other_solution_dictionary.dict.items():
            self.dict[k] = v

    def create_dict(self, guesses, solutions):
        guess_descriptions = map(self.guess_description, guesses, repeat(solutions))
        return {desc.guess_word: desc for desc in guess_descriptions}

    def guess_description(self, guess, solutions):
        return GuessDescription(guess, solutions)

    def create_statistics(self):
        stats = []
        for word in self.dict:
            guess_description = self.dict[word]  # {score -> scoredWords}
            
            number_of_buckets = guess_description.number_of_buckets
            max_words = max(len(bucket) for bucket in guess_description.buckets)
            min_words = min(len(bucket) for bucket in guess_description.buckets)
            avg_words = sum(len(bucket) for bucket in guess_description.buckets) / number_of_buckets
            stat = Statistic(word, number_of_buckets, max_words, min_words, avg_words)
            stats.append(stat)

        def my_key(stat: Statistic):
            return -stat.number_of_buckets

        stats.sort(key=my_key)
        return stats

    def solutions_for(self, guess, score):
        guess_description = self.dict[guess]
        return guess_description.solutions_for(score)
