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
        self.flags_remaining = num_mines
        self.won = False

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

    def get_surrounding_indices(self, y_idx, x_idx):
        idxs = [self.get_cell(y_idx-1, x_idx-1, False),
                self.get_cell(y_idx-1, x_idx, False),
                self.get_cell(y_idx-1, x_idx+1, False),
                self.get_cell(y_idx, x_idx-1, False),
                self.get_cell(y_idx, x_idx+1, False),
                self.get_cell(y_idx+1, x_idx-1, False),
                self.get_cell(y_idx+1, x_idx, False),
                self.get_cell(y_idx+1, x_idx+1, False)]
        return [x for x in idxs if x is not None]


    def get_cell(self, y_idx, x_idx, return_cell=True):
        max_y = len(self.grid) - 1
        max_x = len(self.grid[0]) - 1
        if y_idx < 0 or x_idx < 0 or y_idx > max_y or x_idx > max_x:
            if return_cell:
                return Cell()
            return None
        if return_cell:
            return self.grid[y_idx][x_idx]
        return (y_idx, x_idx)

    def calculate_surrounding(self):
        for y_idx, row in enumerate(self.grid):
            for x_idx, cell in enumerate(row):
                surrounding = self.get_surrounding(y_idx, x_idx)
                cell.num_surrounding = sum([1 for x in surrounding if x.is_mine])

    def flag(self, coords):
        cell = self.grid[coords[0]][coords[1]]
        if cell.is_flag:
            cell.is_flag = False
            self.flags_remaining += 1
        else:
            cell.is_flag = True
            self.flags_remaining -= 1
            if self.flags_remaining < 1:
                self.check_win()

    def clear(self, coords):
        cell = self.grid[coords[0]][coords[1]]
        if cell.is_flag:
            return

        cell.visible = True

        if cell.is_mine:
            self.end()
            print("You lost!")
            return

        if cell.num_surrounding == 0:
            self.reveal_empty_surrounding(coords, [])

    def reveal_empty_surrounding(self, coords, checked):
        cell = self.get_cell(coords[0], coords[1])
        cell.visible = True
        checked.append(coords)
        if cell.num_surrounding == 0 and not cell.is_mine:
            for new_coords in self.get_surrounding_indices(coords[0], coords[1]):
                if new_coords not in checked:
                    checked.append(new_coords)
                    self.reveal_empty_surrounding(new_coords, checked)

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
        if cell[0] < 0 or cell[0] >= len(self.grid[0]):
            return False
        if cell[1] < 0 or cell[1] >= len(self.grid):
            return False
        return True

    def draw(self):
        print('  ', end='')
        print(' '.join([str(x) for x in range(len(self.grid[0]))]))

        for idx, row in enumerate(self.grid):
            print(str(idx) + ' ', end='')
            print(' '.join([str(x) for x in row]))

        print("Flags Remaining: {0}".format(self.flags_remaining))

    def check_win(self):
        if self.flags_remaining > 0:
            return

        for row in self.grid:
            for cell in row:
                if cell.is_flag and not cell.is_mine:
                    return
                if cell.is_mine and not cell.is_flag:
                    return

        self.won = True

g = Game()

g.draw()

while not g.end_flag:
    if g.won:
        print("You won!")
        break
    g.handle_input()
    if g.end_flag:
        break
    g.draw()
