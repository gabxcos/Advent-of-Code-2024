import time
from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class WarehouseSplitter(BaseLinesSplitter):

    @staticmethod
    def get_warehouse(lines):
        lines = [list(l) for l in lines]
        width = len(lines[0])
        height = len(lines)

        walls = []
        robot = None
        boxes = []

        for x in range(0, width):
            for y in range(0, height):
                if lines[y][x]=="#":
                    walls.append( x + 1j * y)
                elif lines[y][x]=="O":
                    boxes.append( x + 1j * y )
                elif lines[y][x]=="@":
                    robot = x + 1j * y

        return (width, height), robot, walls, boxes
    
    @staticmethod
    def convert_move(txt):
        return {
            "^": -1j,
            "v": 1j,
            "<": -1,
            ">": 1
        }[txt]
    
    @staticmethod
    def convert_back_move(move):
        return {
            -1j: "^",
            1j: "v",
            -1: "<",
            1: ">"
        }[move]

    @staticmethod
    def get_moves(lines):
        line = list("".join(lines))
        return [WarehouseSplitter.convert_move(el) for el in line]
    
    def split(self):
        split_index = self.lines.index("")
        warehouse = WarehouseSplitter.get_warehouse(self.lines[:split_index])
        moves = WarehouseSplitter.get_moves(self.lines[split_index+1:])
        return warehouse, moves

    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True, debug: bool = False):
        super().__init__(day=15, raw=True, skip_test=skip_test, elapsed=elapsed, debug=debug)
        self.test_data = WarehouseSplitter(self.test_data).split()
        self.data = WarehouseSplitter(self.data).split()

    def setup(self, data, widened = False):
        warehouse, self.moves = data
        (width, self.height), robot, walls, boxes = warehouse
        

        factor = 2 if widened else 1

        self.width = factor * width
        self.boxes = set([int(b.real * factor) + 1j * int(b.imag) for b in boxes])
        self.walls = set([int(w.real * factor) + 1j * int(w.imag) for w in walls])
        self.robot = int(robot.real * factor) + 1j * int(robot.imag)

        # Sanity checks
        self.og_boxes_num = len(self.boxes)
        self.og_walls_num = len(self.walls)

    def move_robot(self, move):
        new_robot = self.robot + move
        find_air = new_robot
        boxes = []
        while find_air in self.boxes:
            boxes.append(find_air)
            find_air += move
        if find_air not in self.walls:
            if len(boxes) > 0:
                self.boxes.remove(boxes[0])
                self.boxes.add(find_air)
            self.robot = new_robot

    def move_robot_widened(self, move):
        horizontal = (move.imag == 0)

        new_robot = self.robot + move
        find_air = [new_robot + min(int(move.real), 0)] if horizontal else [new_robot, new_robot - 1]
        found_boxes = list(filter(lambda x: (x in self.boxes), find_air))
        boxes = []
        while len(found_boxes)>0:
            boxes.extend(found_boxes)
            find_air = []
            for b in found_boxes:
                if horizontal:
                    find_air.append(b + 2*move)
                else:
                    find_air.extend([b+move, b+move-1, b+move+1])
            find_air = list(set(find_air))
            found_boxes = list(filter(lambda x: (x in self.boxes), find_air))
            found_walls = list(filter(lambda x: (x in self.walls), find_air))
            if len(found_walls)>0:
                break

        # Check walls
        found_walls = list(filter(lambda x: (x in self.walls), find_air))
        if len(found_walls) == 0:
            if len(boxes) > 0:
                new_boxes = set([box + move for box in boxes])
                remove_boxes = set(boxes) - new_boxes
                
                self.boxes = self.boxes - remove_boxes
                self.boxes = self.boxes.union(new_boxes)
            self.robot += move

    def print_grid(self, widened = False):
        for y in range(self.height):
            string = ""
            for x in range(self.width):
                pos = x + 1j * y
                if (pos in self.walls) or (widened and ((pos-1) in self.walls)):
                    string += "#"
                elif ((not widened) and (pos in self.boxes)):
                    string += "O"
                elif (widened and (pos in self.boxes)):
                    string += "["
                elif (widened and ((pos-1) in self.boxes)):
                    string += "]"
                elif pos == self.robot:
                    string += "@"
                else:
                    string += "."
            print(string)
        print("\n\n")

    def part_1(self, data):
        self.setup(data)
        if self.debug: self.print_grid()
        for move in self.moves:
            self.move_robot(move)
            if self.debug:
                time.sleep(0.1)
                print(WarehouseSplitter.convert_back_move(move))
                print(self.robot, "\n")
                self.print_grid()
                
                assert self.og_boxes_num == len(self.boxes), f"Curr boxes num: {len(self.boxes)}, was: {self.og_boxes_num}"
                assert self.og_walls_num == len(self.walls), f"Curr boxes num: {len(self.walls)}, was: {self.og_walls_num}"

        return sum([int(100*box.imag + box.real) for box in self.boxes])
    
    def part_2(self, data):
        self.setup(data, True)
        if self.debug: self.print_grid(True)
        for move in self.moves:
            self.move_robot_widened(move)
            if self.debug:
                time.sleep(0.1)
                print(WarehouseSplitter.convert_back_move(move))
                print(self.robot)
                self.print_grid(True)
                
                assert self.og_boxes_num == len(self.boxes), f"Curr boxes num: {len(self.boxes)}, was: {self.og_boxes_num}"
                assert self.og_walls_num == len(self.walls), f"Curr boxes num: {len(self.walls)}, was: {self.og_walls_num}"

        return sum([int(100*box.imag + box.real) for box in self.boxes])