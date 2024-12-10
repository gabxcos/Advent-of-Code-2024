import os

def puzzle_read(day_string: str, test: bool = False):
    path = os.path.abspath(f"inputs/{'test' if test else 'puzzle'}/{day_string}")
    with open(path, "r") as f:
        lines = [l.replace("\n","") for l in f.readlines()]
    return lines

class BaseLinesSplitter():
    def __init__(self, lines: list[str]):
        self.lines = lines

    def split(self):
        return [list(l) for l in self.lines]