from utils.base_solver import BaseSolver
from utils.puzzle_reader import BaseLinesSplitter

class RulesAndUpdatesSplitter(BaseLinesSplitter):
    def split(self):
        split_index = self.lines.index("")

        rules = [l.split("|") for l in self.lines[:split_index]]
        updates = [l.split(",") for l in self.lines[split_index+1:]]

        return rules, updates


class Solver(BaseSolver):
    def __init__(self, skip_test: bool = False, benchmark: bool = True):
        super().__init__(day=5, raw=True, skip_test=skip_test, benchmark=benchmark)
        self.test_data = RulesAndUpdatesSplitter(self.test_data).split()
        self.data = RulesAndUpdatesSplitter(self.data).split()

    @staticmethod
    def check_rule(update, rule):
        x,y = rule

        if (x in update) and (y in update):
            x_i = update.index(x)
            y_i = update.index(y)
            return (x_i < y_i)
        else:
            return True
        
    @staticmethod
    def check_rules(update, rules):
        for rule in rules:
            if not Solver.check_rule(update, rule): return False
        return True
    
    @staticmethod
    def sort_update(update, rules):
        prev_update = list(update)
        valid_rules = [r for r in rules if (r[0] in update) and (r[1] in update)]

        rules_dict = {}
        for x,y in valid_rules:
            if x not in rules_dict:
                rules_dict[x] = [y]
            else:
                rules_dict[x].append(y)
        
        adj_list = { k : len(rules_dict[k]) for k in rules_dict}
        semi_last = [k for k in rules_dict if adj_list[k]==1][0]
        adj_list.update({rules_dict[semi_last][0] : 0})

        new_update = prev_update
        new_update.sort(key = lambda x : adj_list[x], reverse = True)
        
        return new_update

    def part_1(self, data):
        rules, updates = data

        counter = 0

        for update in updates:
            ok = True
            for rule in rules:
                if not Solver.check_rule(update, rule):
                    ok = False
                    break
            if ok:
                counter += int(update[len(update) // 2])

        return counter
    
    def part_2(self, data):
        rules, updates = data

        counter = 0

        for update in updates:
            if not Solver.check_rules(update, rules):
                update = Solver.sort_update(update, rules)
                counter += int(update[len(update) // 2])
        return counter