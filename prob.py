import random
import collections
from operator import itemgetter


class ProbabilityCounter():

    def __init__(self, counter):
        self._counter = counter
        self._probabilities = []

        total_count = sum(counter.values())
        for (key, n_key) in counter.items():
            self._probabilities.append((key, n_key / total_count))

        self._probabilities = sorted(self._probabilities,
                                     key=itemgetter(1),
                                     reverse=True)

        sum_probability = 0
        for i in range(len(self._probabilities)):
            (key, prob) = self._probabilities[i]
            sum_probability += prob
            self._probabilities[i] = (key, sum_probability)

        self._keys = [key for (key, _) in self._probabilities]

    def keys(self):
        return self._keys

    def get(self):
        """Returns a random value based on its probability of occuring in given data set."""
        random_value = random.random()
        for (key, prob) in self._probabilities:
            if random_value <= prob:
                return key
        return self._probabilities[-1][0]
