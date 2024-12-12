# The thrashed, non-working version is under the `trashed` folder. External help was used for coming up with this solution.
from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter
import re
from itertools import combinations

class PlaceboSplitter(BaseLinesSplitter):
    def split(self):
        return self.lines
    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=12, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = PlaceboSplitter(self.test_data).split()
        self.data = PlaceboSplitter(self.data).split()

    def is_valid(self, coords: complex):
        return int(coords.real) in range(self.length) and int(coords.imag) in range(self.width)
    
    def get_element(self, coords: complex) -> str:
        return self.lines[int(coords.imag)][int(coords.real)]

    def get_crop_recursive(self, coordinate:complex, to_match:str):
        if coordinate in self.matched:
            return
        self.matched.append(coordinate)
        for i in range(4):
            new_element = coordinate-(1j)**i
            if self.is_valid(new_element) and self.get_element(new_element)==to_match:
                self.get_crop_recursive(new_element, to_match)
        return

    def get_crop(self, coordinate: complex):
        self.matched = []
        to_match = self.get_element(coordinate)
        self.get_crop_recursive(coordinate, to_match)
        return self.matched

    def setup(self, data):
        self.lines = data
        self.length = len(self.lines[0])
        self.width = len(self.lines)

        string = ''.join(self.lines)
        self.possible_characters = set(string)

        self.regions=[]
        for character in self.possible_characters:
            coordinates=[complex(*divmod(i, self.width)[::-1]) for i in (i.start() for i in re.finditer(character, string))]
            for coord in coordinates:
                if coord not in [coord for region in self.regions for coord in region]:
                    self.regions.append(self.get_crop(coord))

    def part_1(self, data):
        self.setup(data)
        cost=0
        for region in self.regions:
            surroundings=[(i, (1j)**_ ) for i in region for _ in range(4) if i+(1j)**_ not in region]
            perimeter=len(surroundings)
            area=len(region)
            cost+=perimeter*area
        return cost
    
    def part_2(self, data):
        self.setup(data)
        cost=0
        for region in self.regions:
            surroundings=[(i, (1j)**_ ) for i in region for _ in range(4) if i+(1j)**_ not in region]
            count=0
            plausible_differences=[1, 1j, -1, -1j]
            for element1, element2 in combinations(surroundings, 2):
                if element1[0]-element2[0] in plausible_differences and element1[1]==element2[1]:
                    count+=1
            sides=len(surroundings)-count
            area=len(region)
            cost+=sides*area
        return cost