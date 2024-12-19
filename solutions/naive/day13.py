from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter


class MachineSplitter(BaseLinesSplitter):
    @staticmethod
    def get_move(string, prize=False):
        split_char = "=" if prize else "+"
        x = int(string.split(split_char)[1].split(",")[0])
        y = int(string.split(split_char)[-1])
        return x + y * 1j

    def get_machine(self, i):
        A_move = MachineSplitter.get_move(self.lines[4 * i])
        B_move = MachineSplitter.get_move(self.lines[4 * i + 1])
        prize_move = MachineSplitter.get_move(self.lines[4 * i + 2], True)
        return [A_move, B_move, prize_move]

    def split(self):
        iterations = (len(self.lines) + 1) // 4
        return [self.get_machine(i) for i in range(iterations)]


class Solver(BaseSolver):
    def __init__(
        self, skip_test: bool = False, elapsed: bool = True, debug: bool = False
    ):
        super().__init__(
            day=13, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug
        )
        self.test_data = MachineSplitter(self.test_data).split()
        self.data = MachineSplitter(self.data).split()

    @staticmethod
    def solve_equation_machine(machine, part1=True):
        A_move, B_move, prize_move = machine
        mAx, mBx, px = (int(el.real) for el in (A_move, B_move, prize_move))
        mAy, mBy, py = (int(el.imag) for el in (A_move, B_move, prize_move))

        if not part1:
            px += 10_000_000_000_000
            py += 10_000_000_000_000

        try:
            B = (px * mAy - py * mAx) / (mBx * mAy - mBy * mAx)
            A = (px - mBx * B) / mAx
            if (B % 1 < 1e-9) and (A % 1 < 1e-9):
                A = int(A)
                B = int(B)
            else:
                return 0
            if (A > 0) and (B > 0):
                if part1:
                    if (A >= 100) or (B >= 100):
                        return 0
                return A * 3 + B
            else:
                return 0
        except:
            return 0

    def part_1(self, data):
        return sum([Solver.solve_equation_machine(machine) for machine in data])

    def part_2(self, data):
        return sum(
            [Solver.solve_equation_machine(machine, part1=False) for machine in data]
        )
