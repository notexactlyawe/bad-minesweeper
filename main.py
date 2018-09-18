import pdb
import random
import itertools

class Cell():
    def __init__(self, is_mine=False):
        self.is_mine = is_mine
        self.is_flag = False
        self.visible = False
        self.num_surrounding = 0

    def __str__(self):
        if self.is_flag:
            return '>'
        if not self.visible:
            return '~'
        if self.is_mine:
            return 'x'
        return str(self.num_surrounding)

class Game():
    def __init__(self, size=(10, 10), num_mines=20):
        self.end_flag = False
        self.ACCEPTED_INSTRUCTIONS = {"flag": self.flag, "clear": self.clear, "end": self.end}
        self.grid = []
        for row in range(size[0]):
            temp = []
            for col in range(size[1]):
                temp.append(Cell())
            self.grid.append(temp)
        self.first_input = True
        self.num_mines = num_mines

    def lay_mines(self, num_mines, ignore=None):
        width = len(self.grid[0])
        height = len(self.grid)
        poss_co_ords = list(itertools.product(range(height), range(width)))

        if ignore is not None:
            poss_co_ords.remove(ignore)

        for mine in range(num_mines):
            mine_location = random.choice(poss_co_ords)
            poss_co_ords.remove(mine_location)
            self.grid[mine_location[0]][mine_location[1]].is_mine = True

    def get_surrounding(self, y_idx, x_idx):
        return [self.get_cell(y_idx-1, x_idx-1),
                self.get_cell(y_idx-1, x_idx),
                self.get_cell(y_idx-1, x_idx+1),
                self.get_cell(y_idx, x_idx-1),
                self.get_cell(y_idx, x_idx+1),
                self.get_cell(y_idx+1, x_idx-1),
                self.get_cell(y_idx+1, x_idx),
                self.get_cell(y_idx+1, x_idx+1)]

    def get_cell(self, y_idx, x_idx):
        try:
            return self.grid[y_idx][x_idx]
        except:
            return Cell()

    def calculate_surrounding(self):
        for y_idx, row in enumerate(self.grid):
            for x_idx, cell in enumerate(row):
                surrounding = self.get_surrounding(y_idx, x_idx)
                cell.num_surrounding = sum([1 for x in surrounding if x.is_mine])

    def flag(self, cell):
        self.grid[cell[1]][cell[0]].is_flag = True

    def clear(self, cell):
        cell = self.grid[cell[1]][cell[0]]
        if cell.is_flag:
            return

        cell.visible = True

        if cell.is_mine:
            self.end()
            return

    def end(self):
        self.end_flag = True

    def handle_input(self):
        handled = False

        while not handled:
            raw_in = input("> ").strip()
            if raw_in == "end":
                self.end()
                return

            split_input = raw_in.split()
            if not self.input_is_acceptable(split_input):
                self.print_instructions()
                continue

            cell = [0, 0]

            try:
                cell[0] = int(split_input[1])
                cell[1] = int(split_input[2])
            except Exception as e:
                print(e)

            if not self.check_cell(cell):
                self.print_instructions()
                continue

            if self.first_input and split_input[0] == 'clear':
                self.lay_mines(self.num_mines, ignore=tuple(cell))
                self.calculate_surrounding()
                self.first_input = False

            self.ACCEPTED_INSTRUCTIONS[split_input[0]](cell)
            handled = True

    def print_instructions(self):
        print("Please enter one of the following instructions followed by the cell")
        print("\n".join(self.ACCEPTED_INSTRUCTIONS))

    def input_is_acceptable(self, split_input):
        return len(split_input) == 3 and split_input[0] in self.ACCEPTED_INSTRUCTIONS

    def check_cell(self, cell):
        if cell[0] < 0 or cell[0] > len(self.grid[0]):
            return False
        if cell[1] < 0 or cell[1] > len(self.grid):
            return False
        return True

    def draw(self):
        for row in self.grid:
            for column in row:
                print(column, end="")
            print()

g = Game()

g.draw()

while not g.end_flag:
    g.handle_input()
    if g.end_flag:
        break
    g.draw()
