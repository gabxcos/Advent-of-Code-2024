from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class AlternateSplitter(BaseLinesSplitter):
    def split(self):
        int_list = [int(l) for l in list(self.lines[0])]
        return [ int_list[0::2], int_list[1::2] ]
    
class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, elapsed: bool = True):
        super().__init__(day=9, raw=True, skip_test=skip_test, elapsed=elapsed)
        self.test_data = AlternateSplitter(self.test_data).split()
        self.data = AlternateSplitter(self.data).split()


    @staticmethod
    def rightmost_number_index(map):
        for i in range(len(map))[-1 : 0 : -1]:
            if map[i]: return i


    @staticmethod    
    def leftmost_none_index(map):
        return map.index(None)
    

    @staticmethod
    def swap(map, li, ri):
        tmp = (map[li], map[ri])
        map[ri] = tmp[0]
        map[li] = tmp[1]
        return map

    def part_1(self, data):
        files, spaces = data
        spaces.append(0) # in order to have an identical count for both

        i = 0
        map = []
        for file, space in zip(files, spaces):
            map.extend([i] * file)
            map.extend([None] * space)
            i += 1
        
        for _ in map:
            ri = Solver.rightmost_number_index(map)
            li = Solver.leftmost_none_index(map)
            if ri > li:
                map = Solver.swap(map, li, ri)
            else:
                break

        map = list(filter(lambda x:(x is not None), map))
        
        counts = [i*el for i,el in enumerate(map)]
        
        return sum(counts)
    
    def part_2(self, data):
        files, spaces = data
        spaces.append(0) # in order to have an identical count for both

        n = 0
        map = []
        for file, space in zip(files, spaces):
            map.append( (n, file, space) )
            n += 1

        while True:
            do_stop = True
            for i_A, (n_A, file_A, space_A) in enumerate(map[::-1]):
                i_A = len(map) - 1 - i_A
                if (i_A < 1): break
                if (n_A < 0): continue
                can_fit = False
                for i_B, (n_B, file_B, space_B) in enumerate(map[:i_A]):
                    if (n_B < 0): continue
                    if file_A <= space_B:
                        can_fit = True
                        do_stop = False
                        break
                if can_fit: break
            if do_stop: break
            else:
                map[i_B] = (n_B, file_B, 0)
                map[i_A] = (-1, 0, file_A + space_A)
                map.insert(i_B + 1, (n_A, file_A, space_B - file_A))

        i = 0
        counter = 0
        for n, file, space in map:
            n = max(n, 0)
            for _ in range(file):
                counter += n * i
                i += 1
            i += space

        return counter

        map = list(filter(lambda x:(x is not None), map))
        
        counts = [i*el for i,el in enumerate(map)]
        
        return sum(counts)