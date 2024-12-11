from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class MatrixIntSplitter(BaseLinesSplitter):
    def split(self):
        return [[int(el) for el in list(l)] for l in self.lines]
    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=10, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MatrixIntSplitter(self.test_data).split()
        self.data = MatrixIntSplitter(self.data).split()

    @staticmethod
    def iterate(data, zero_pos, distinct = False):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        candidates = [zero_pos]
        for i in range(1, 10):
            new_candidates = []
            for x,y in candidates:
                new_candidates.extend([(x+d[0], y+d[1]) for d in directions])
            new_candidates = list(filter(lambda pos: Solver.check(data, pos, i), new_candidates))
            if len(new_candidates)==0: return 0
            else: candidates = new_candidates
        if not distinct: candidates = list(set(candidates))
        return len(candidates)

    @staticmethod
    def check(data, pos, num):
        x, y = pos
        if (0 <= x < len(data[0])) and (0 <= y < len(data)):
            return (data[y][x] == num)
        return False

    def part_1(self, data):
        counter = 0
        for x in range(len(data[0])):
            for y in range(len(data)):
                if data[y][x] == 0:
                    counter += Solver.iterate(data, (x, y))
        return counter
    
    def part_2(self, data):
        counter = 0
        for x in range(len(data[0])):
            for y in range(len(data)):
                if data[y][x] == 0:
                    counter += Solver.iterate(data, (x, y), True)
        return counter