from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter
from functools import partial

class Infix(object):
    def __init__(self, func):
        self.func = func
    def __or__(self, other):
        return self.func(other)
    def __ror__(self, other):
        return Infix(partial(self.func, other))
    def __call__(self, v1, v2):
        return self.func(v1, v2)
    
@Infix
def concat(x, y):
    return int(str(x) + str(y))


class TupleSplitter(BaseLinesSplitter):
    def split(self):
        return [[int(num) for num in l.replace(":","").split(" ")] for l in self.lines]

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, benchmark: bool = True):
        super().__init__(day=7, raw=True, skip_test=skip_test, benchmark=benchmark)
        self.test_data = TupleSplitter(self.test_data).split()
        self.data = TupleSplitter(self.data).split()

    @staticmethod
    def operations(op_1, op_2, with_concat = False):
        results = [op_1 + op_2, op_1 * op_2]
        if with_concat: results.append( op_1 |concat| op_2)
        return results


    @staticmethod
    def compute(data, with_concat = False):
        counter = 0

        for line in data:
            res = line[0]
            operands = line[1:]

            candidates = [operands[0]]
            i = 1
            while i < len(operands):
                new_operand = operands[i]
                tmp_results = []
                for c in candidates:
                    tmp_results.extend(Solver.operations(c, new_operand, with_concat))
                candidates = list(filter(lambda x : x <= res, tmp_results))
                i += 1
            
            if candidates.count(res)>0: counter += res
        
        return counter

    def part_1(self, data):
        return Solver.compute(data)
    
    def part_2(self, data):
        return Solver.compute(data, True)