from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class PlaceboSplitter(BaseLinesSplitter):
    def split(self):
        return self.lines

class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=4, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = PlaceboSplitter(self.test_data).split()
        self.data = PlaceboSplitter(self.data).split()

        # Shared variables
        self.counter = 0
        self.lines = self.data

    def check_on_coordinates(self, M_coord, A_coord, S_coord):
        M_x, M_y = M_coord
        A_x, A_y = A_coord
        S_x, S_y = S_coord

        check = False
        if all([coord >= 0 for coord in [M_x, M_y, A_x, A_y, S_x, S_y]]):
            try:
                if (self.lines[M_y][M_x]=="M") and (self.lines[A_y][A_x]=="A") and (self.lines[S_y][S_x]=="S"): check = True
            except:
                pass

            if check: self.counter += 1

    
    def check_on_coordinates_MAS(self, M_coord, S_coord):
        M_x, M_y = M_coord
        S_x, S_y = S_coord

        check = False
        if all([coord >= 0 for coord in [M_x, M_y, S_x, S_y]]):
            try:
                if (self.lines[M_y][M_x]=="M") and (self.lines[S_y][S_x]=="S"): check = True
                elif (self.lines[M_y][M_x]=="S") and (self.lines[S_y][S_x]=="M"): check = True
            except:
                pass

        return check

    def all_directions(self, x, y):
        # Forward
        self.check_on_coordinates((x+1, y), (x+2, y), (x+3, y))
        # Backward
        self.check_on_coordinates((x-1, y), (x-2, y), (x-3, y))
        # Up
        self.check_on_coordinates((x, y-1), (x, y-2), (x, y-3))
        # Down
        self.check_on_coordinates((x, y+1), (x, y+2), (x, y+3))
        # Forward up
        self.check_on_coordinates((x+1, y-1), (x+2, y-2), (x+3, y-3))
        # Forward down
        self.check_on_coordinates((x+1, y+1), (x+2, y+2), (x+3, y+3))
        # Backward up
        self.check_on_coordinates((x-1, y-1), (x-2, y-2), (x-3, y-3))
        # Backward down
        self.check_on_coordinates((x-1, y+1), (x-2, y+2), (x-3, y+3))


    def cross_MAS(self, x, y):
        combos = (
            ( (x-1, y-1), (x+1, y+1) ),
            ( (x+1, y-1), (x-1, y+1))
        )

        num_matches = [1 for (M_coord, S_coord) in combos if self.check_on_coordinates_MAS(M_coord, S_coord)]
        if sum(num_matches)==2: self.counter+=1

    def part_1(self, data):
        self.counter = 0
        self.lines = data

        num_lines = len(self.lines)
        line_length = len(self.lines[0])

        for y in range(num_lines):
            for x in range(line_length):
                if self.lines[y][x] == "X":
                    self.all_directions(x, y)
        
        return self.counter
    
    def part_2(self, data):
        self.counter = 0
        self.lines = data

        num_lines = len(self.lines)
        line_length = len(self.lines[0])

        for y in range(num_lines):
            for x in range(line_length):
                if self.lines[y][x] == "A":
                    self.cross_MAS(x, y)
        
        return self.counter