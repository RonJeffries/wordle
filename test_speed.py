import time
from concurrent.futures import ProcessPoolExecutor
from math import floor, sqrt

import pytest


def is_prime(number):
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    limit = floor(sqrt(number)) + 1
    for i in range(3, limit, 2):
        if number % i == 0:
            return False
    return True


class TestSpeed:
    NUMBERS = [17977, 10619863, 106198, 6620830889, 80630964769, 228204732751,
               1171432692373, 1398341745571, 10963707205259, 15285151248481,
               99999199999, 304250263527209, 30425026352720, 10657331232548839,
               10657331232548830, 44560482149, 1746860020068409,
               17977, 10619863, 106198, 6620830889, 80630964769, 228204732751,
               1171432692373, 1398341745571, 10963707205259, 15285151248481,
               99999199999, 304250263527209, 30425026352720, 10657331232548839,
               10657331232548830, 44560482149, 1746860020068409,17977, 10619863, 106198, 6620830889, 80630964769, 228204732751,
               1171432692373, 1398341745571, 10963707205259, 15285151248481,
               99999199999, 304250263527209, 30425026352720, 10657331232548839,
               10657331232548830, 44560482149, 1746860020068409,
               17977, 10619863, 106198, 6620830889, 80630964769, 228204732751,
               1171432692373, 1398341745571, 10963707205259, 15285151248481,
               99999199999, 304250263527209, 30425026352720, 10657331232548839,
               10657331232548830, 44560482149, 1746860020068409,17977, 10619863, 106198, 6620830889, 80630964769, 228204732751,
               1171432692373, 1398341745571, 10963707205259, 15285151248481,
               99999199999, 304250263527209, 30425026352720, 10657331232548839,
               10657331232548830, 44560482149, 1746860020068409,
               17977, 10619863, 106198, 6620830889, 80630964769, 228204732751,
               1171432692373, 1398341745571, 10963707205259, 15285151248481,
               99999199999, 304250263527209, 30425026352720, 10657331232548839,
               10657331232548830, 44560482149, 1746860020068409,17977, 10619863, 106198, 6620830889, 80630964769, 228204732751,
               1171432692373, 1398341745571, 10963707205259, 15285151248481,
               99999199999, 304250263527209, 30425026352720, 10657331232548839,
               10657331232548830, 44560482149, 1746860020068409,
               17977, 10619863, 106198, 6620830889, 80630964769, 228204732751,
               1171432692373, 1398341745571, 10963707205259, 15285151248481,
               99999199999, 304250263527209, 30425026352720, 10657331232548839,
               10657331232548830, 44560482149, 1746860020068409,
               ]

    def test_numbers_size(self):
        assert len(self.NUMBERS) == 136

    @pytest.mark.skip("20 seconds is too long")
    def test_primes(self):
        t0 = time.time()
        results = self.check_numbers_prime()
        count = sum(1 for result in results if result[1])
        delta_time = time.time() - t0
        assert count == 112
        assert delta_time > 19

    def check_numbers_prime(self):
        return zip(self.NUMBERS, map(is_prime, self.NUMBERS))

    def check_numbers_prime_concurrently(self):
        with ProcessPoolExecutor() as executor:
            results = executor.map(is_prime, self.NUMBERS)
        return zip(self.NUMBERS, results)

    @pytest.mark.skip("5 seconds is also too long")
    def test_primes_parallel(self):
        t0 = time.time()
        results = self.check_numbers_prime_concurrently()
        count = sum(1 for result in results if result[1])
        delta_time = time.time() - t0
        assert count == 112
        assert delta_time < 5

    def test_iterator_once_only(self):
        result = map(lambda i: i*2,  range(3))
        vals = list(result)
        assert vals == [0, 2, 4]
        again = list(result)
        assert again == []

    def func(self, r):
        return 2*r

    def test_parallel_range(self):
        r = range(8)
        with ProcessPoolExecutor(8) as exec:
            parallel_results = exec.map(self.func, r)
        parallel_list = list(parallel_results)
        serial_results = map(self.func, r)
        serial_list = list(serial_results)
        expected_list = [0, 2, 4, 6, 8, 10, 12, 14]
        assert serial_list == parallel_list
        assert parallel_list == expected_list

    def process_chunk(self, guesses):
        return map(lambda g: g+":yes", guesses)

    def do_chunk(self, chunk):
        guesses = ["a", "b", "c", "d", "e", "f", "g", "h"]
        begin = chunk[0]
        end = begin + chunk[1]
        s = slice(begin, end)
        items = guesses[s]
        return self.process_chunk(items)

    def test_parallel_chunker(self):
        chunks = [(0, 2), (2, 2), (4, 2), (6, 2)]
        result = map(self.do_chunk, chunks)
        expected = [x+":yes" for x in "abcdefgh"]
        results = [item for sublist in result for item in sublist]
        assert results == expected

