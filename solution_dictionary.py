from scored_words import ScoredWords


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


class SolutionDictionary:
    def __init__(self, guesses, solutions):
        self.dict = self.create_dict(guesses, solutions)

    @staticmethod
    def create_dict(guesses, solutions):
        solutions_dict = {}  # guess -> dict (score -> [solutions])
        for guess in guesses:
            guess_dict = {}  # score -> [solutions]
            solutions_dict[guess] = guess_dict
            for solution in solutions:
                score = guess.score(solution)
                if not score in guess_dict:
                    guess_dict[score] = ScoredWords(score)
                guess_dict[score].add_word(solution)
        return solutions_dict

    def create_statistics(self):
        stats = []
        for word in self.dict:
            word_dict = self.dict[word]  # {score -> scoredWords}
            
            number_of_buckets = len(word_dict)
            max_words = max(len(bucket) for bucket in word_dict.values())
            min_words = min(len(bucket) for bucket in word_dict.values())
            avg_words = sum(len(bucket) for bucket in word_dict.values()) / number_of_buckets
            stat = Statistic(word, number_of_buckets, max_words, min_words, avg_words)
            stats.append(stat)

        def my_key(stat: Statistic):
            return -stat.number_of_buckets

        stats.sort(key=my_key)
        return stats

    def solutions_for(self, guess, score):
        try:
            return self.dict[guess][score]
        except KeyError:
            return []
