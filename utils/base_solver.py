from inputs.test.solutions import test_solutions
from utils.puzzle_reader import puzzle_read
from datetime import timedelta
import time

class BaseSolver:
    def __init__(self, day: int = -1, raw: bool = True, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        self.day = day
        self.day_string = str(day).zfill(2)
        self.raw = raw
        self.skip_test = skip_test
        self.elapsed = elapsed
        self.debug = debug
        self.test_data = puzzle_read(day_string=self.day_string, test=True)
        self.test_solutions = test_solutions.get(self.day_string, [None, None])
        self.data = puzzle_read(self.day_string)

    def test(self, part: int = 1):
        func = getattr(self, f"part_{part}")
        result = func(self.test_data)
        sol = self.test_solutions[part-1]
        if (sol is None):
            print("No test available, computed:", result)
            return True
        elif result==sol:
            print("Test passed!")
            return True
        else:
            print("Test failed!")
            print(f"- Expected: {self.test_solutions[part-1]}")
            print(f"- Computed: {result}")
            return False
        

    def solve(self, part: int = 1):
        if not self.skip_test:
            assert self.test(part), f"Can't solve part {part} without passing the test first!"

        func = getattr(self, f"part_{part}")

        start = time.time()
        result = func(self.data)
        elapsed = time.time() - start

        print(f"Computed solution: {result}")
        if self.elapsed: print(f"Time elapsed: {timedelta(seconds=elapsed)}")
        print()
        
        return result

