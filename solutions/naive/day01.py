from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class CoupleSplitter(BaseLinesSplitter):
    def split(self):
        return [(int(l.split(" ")[0]), int(l.split(" ")[-1])) for l in self.lines]

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, benchmark: bool = True):
        super().__init__(day=1, raw=True, skip_test=skip_test, benchmark=benchmark)
        self.test_data = CoupleSplitter(self.test_data).split()
        self.data = CoupleSplitter(self.data).split()

    def part_1(self, data):
        left, right = zip(*data)
        diffs = [abs(el[0] - el[1]) for el in zip(sorted(left), sorted(right))]
        return sum(diffs)
    
    def part_2(self, data):
        left, right = zip(*data)
        similarities = [el * right.count(el) for el in left]
        return sum(similarities)