---
name: Optimization
about: Present a new optimal solution for a given day of AoC 2024
title: "[OPTIMAL] Day 01 Parts 1-2"
labels: optimization
assignees: ''

---

Please try to provide the solution in the same formats as the existing ones.

- There should be a class extending `BaseLinesSplitter` that provides a pre-process to the input (as-is `self.lines` is just the puzzle input read with Python's `File.readlines()` with newline characters after each line `\n` already removed)

```python
from utils.puzzle_reader import BaseLinesSplitter

class PlaceboSplitter(BaseLinesSplitter):
    def split(self):
        return self.lines
```

- There should be a `Solver` class extending `BaseSolver` that:
  - specifies the given day in its' `super().__init__`
  - passes both `self.test_data` and `self.data` through the previously defined `BaseLinesSplitter` child
  - defines any necessary support class or static method
  - defines two class methods, one for each part, taking `data` as input: `part_1(self, data)` and `part_2(self, data`

```python
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True):
        super().__init__(day=4, raw=True, skip_test=skip_test, elapsed=elapsed)
        self.test_data = PlaceboSplitter(self.test_data).split()
        self.data = PlaceboSplitter(self.data).split()

        # (You can define class properties, in order to use only class methods)
        self.counter = 0
        self.lines = self.data

    def utils_1(self, params):
        ...

    def utils_2(self, params):
       ...

    def part_1(self, data):
        self.counter = 0
        self.lines = data

        ...
        
        return self.counter
    
    def part_2(self, data):
        self.counter = 0
        self.lines = data

        ...
        
        return self.counter
```
