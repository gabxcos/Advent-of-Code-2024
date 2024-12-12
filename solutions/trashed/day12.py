from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class MatrixSplitter(BaseLinesSplitter):
    def split(self):
        return [list(l) for l in self.lines]
    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=12, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = MatrixSplitter(self.test_data).split()
        self.data = MatrixSplitter(self.data).split()

    def setup(self, data):
        self.lines = data
        self.width = len(self.lines[0])
        self.height = len(self.lines)
        self.visited = set()
        self.crops = []


    def get_next(self, node, all = False):
        x, y = node

        next_ones = []

        if all:
            dirs = []
            for d_x in [-1, 0, 1]:
                for d_y in [-1, 0, 1]:
                    if (d_x == 0) and (d_y == 0): continue
                    dirs.append((d_x, d_y))
        else:
            dirs = [ (-1, 0), (0, -1), (1, 0), (0, 1) ]
        
        for d_x, d_y in dirs:
            new_x = x+d_x
            new_y = y+d_y
            if (0 <= new_x < self.width) and (0 <= new_y < self.height):
                next_ones.append( (new_x, new_y) )
        return next_ones
    
    def get_neighbours(self, node):
        x, y = node
        val = self.lines[y][x]

        next_ones = self.get_next(node)
        neighbours = [n for n in next_ones if self.lines[n[1]][n[0]]==val]
        return neighbours


    def get_crop(self, node):
        neighbours = self.get_neighbours(node)
        crop_visited = [node] + neighbours
        while len(neighbours)>0:
            new_neighbours = []
            for n in neighbours:
                new_neighbours.extend(self.get_neighbours(n))
            new_neighbours = [n for n in list(set(new_neighbours)) if (n not in crop_visited)]
            crop_visited.extend(new_neighbours)
            neighbours = new_neighbours
            if len(new_neighbours)==0:
                break

        return crop_visited


    def get_perimeter(self, crop):
        return sum([(4 - len(self.get_neighbours(n))) for n in crop])
    
    def get_external_sides(self, crop):
        num_sides = 1
        curr_dir = 0
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        def sum_dir(n, dir):
            return (n[0]+dir[0], n[1]+dir[1])

        first_n = sorted(crop, key = lambda x : x[1]*self.width+x[0])[0]
        curr_n = first_n
        initial = True
        visited = set()
        passes = 0
        while True:
            visited.add(curr_n)
            next_candidates = [
                sum_dir(curr_n, directions[curr_dir]), # up
                sum_dir(curr_n, directions[(curr_dir+1)%4]), # right
                sum_dir(curr_n, directions[(curr_dir+2)%4]), # down
                sum_dir(curr_n, directions[(curr_dir+3)%4]) # left
            ]
            for i, c in enumerate(next_candidates):
                if c in crop:
                    if i == 0: # right to up
                        curr_dir = (curr_dir-1)%4
                        num_sides += 1
                    elif i == 1: # right to right
                        pass
                    elif i == 2: #right to down
                        curr_dir = (curr_dir+1)%4
                        num_sides += 1
                    else: # right to left
                        curr_dir = (curr_dir+2)%4
                        num_sides += 2
                    curr_n = c
                    break
            if (not initial) and (curr_n == first_n):
                next_moves = [n for n in [
                    sum_dir(curr_n, directions[curr_dir]), # up
                    sum_dir(curr_n, directions[(curr_dir+1)%4]), # right
                    sum_dir(curr_n, directions[(curr_dir+2)%4]), # down
                    sum_dir(curr_n, directions[(curr_dir+3)%4]) # left
                ] if (n in crop)]
                if all([(n in visited) for n in next_moves]):
                    break
            initial = False
            passes += 1

            if passes > len(crop) * 4:
                print("Stuck in loop!")
                print(crop)
                exit()

        if curr_dir == 2:
            return num_sides+1
        elif curr_dir == 3:
            return num_sides
        else:
            print("How did we get here?")
            print(crop)
            exit()
        
    def find_crop_from_node(self, node):
        for crop in [v["crop"] for v in self.crops_dict.values()]:
            if node in crop:
                return crop
        print("How did we get here?")
        exit()
        
    def contains_crop(self, main_crop, other_crop):
        for n in other_crop:
            next_ones_with_angles = self.get_next(n, True)
            if len(next_ones_with_angles)<8: # corner or not fully inglobated
                return False
            
            next_ones = self.get_next(n, False)
            for new_n in next_ones:
                if (new_n not in main_crop) and (new_n not in other_crop):
                    if not self.contains_crop(other_crop, self.find_crop_from_node(new_n)):
                        return False
        return True
        
    def get_all_sides(self, crop_hash):
        if self.crops_dict[crop_hash]["sides"] is not None:
            return self.crops_dict[crop_hash]["sides"]
        
        if self.crops_dict[crop_hash]["area"]==1:
            external_sides = 4
            internal_sides = 0
        else:
            main_crop = self.crops_dict[crop_hash]["crop"]

            external_sides = self.get_external_sides(main_crop)

            internal_sides = 0
            for h in self.crops_dict:
                if h != crop_hash:
                    other_crop = self.crops_dict[h]["crop"]
                    if self.contains_crop(main_crop, other_crop):
                        self.get_all_sides(h)
                        internal_sides += self.crops_dict[h]["external_sides"]
            
        sides = external_sides + internal_sides
        self.crops_dict[crop_hash]["sides"] = sides
        self.crops_dict[crop_hash]["external_sides"] = external_sides
        self.crops_dict[crop_hash]["internal_sides"] = internal_sides
        return sides
            
    
    def part_1(self, data):
        self.setup(data)
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) not in self.visited:
                    crop = self.get_crop( (x,y) )
                    self.crops.append(crop)
                    for _x,_y in crop:
                        self.visited.add( (_x, _y) )

        if self.debug:
            for crop in self.crops:
                print(f"{self.lines[crop[0][1]][crop[0][0]]} : {crop} : area = {len(crop)}, perimeter = {self.get_perimeter(crop)}")

        return sum([ len(crop) * self.get_perimeter(crop) for crop in self.crops ])
    
    def part_2(self, data):
        self.setup(data)
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) not in self.visited:
                    crop = self.get_crop( (x,y) )
                    self.crops.append(crop)
                    for _x,_y in crop:
                        self.visited.add( (_x, _y) )

        self.crops_dict = {hash(str(crop)): {"crop": crop, "sides": None, "area": len(crop)} for crop in self.crops}

        if self.debug: print(len(self.crops_dict), "crops to process!")

        counter = 0
        for h in self.crops_dict:
            if self.crops_dict[h]["sides"] is None:
                self.get_all_sides(h)
            counter += 1
            if self.debug: print(counter)

        if self.debug:
            for v in self.crops_dict.values():
                print(v)

        return sum([v["area"] * v["sides"] for v in list(self.crops_dict.values())])