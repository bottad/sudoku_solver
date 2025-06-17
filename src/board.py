import json
import random
from colorama import init, Fore, Style
init(autoreset=True)

class Cell:
    def __init__(self):
        self.options = set(range(1, 10))
        self.entropy = len(self.options)
        self.collapsed_value = None
        self.guessed = False

    def update_entropy(self):
        if self.entropy != 0:
            self.entropy = len(self.options)

    def remove_option(self, val):
        """Remove a single option from the options set, if it exists."""
        if val in self.options:
            self.options.remove(val)
            self.update_entropy()

    def collapse(self, val):
        """Set the cell to a fixed value (collapse it)."""
        if val in self.options:
            self.options = {val}
            self.collapsed_value = val
            self.entropy = 0
        else:
            raise ValueError(f"Cannot collapse to {val} because it's not in options")

class Board:
    def __init__(self):
        self.grid = [[Cell() for _ in range(9)] for _ in range(9)]
        self.solved_cells = 0


    def __str__(self):
        lines = []
        for line_idx in range(27):
            row = line_idx // 3
            inner_line = line_idx % 3

            line_parts = []
            for block_col in range(3):
                block_cells = []
                for col in range(block_col * 3, block_col * 3 + 3):
                    cell = self.grid[row][col]

                    if cell.entropy == 0:
                        # entropy one: special printing
                        if inner_line == 1:
                            # Print the single value padded with spaces on both sides, 5 chars wide total
                            if cell.guessed:
                                block_cells.append(f"  {Fore.YELLOW}{cell.collapsed_value}{Style.RESET_ALL}  ")  # 7 chars wide
                            else:
                                block_cells.append(f"  {Fore.GREEN}{cell.collapsed_value}{Style.RESET_ALL}  ")  # 7 chars wide
                        else:
                            # first and third line: just spaces of width 5
                            block_cells.append("     ")
                    else:
                        # Normal behavior: print options sliced by line
                        opts = list(cell.options)
                        start = inner_line * 3
                        sliced_opts = opts[start:start+3]

                        # Pad with spaces if less than 3 options
                        while len(sliced_opts) < 3:
                            sliced_opts.append(' ')

                        block_cells.append(" ".join(str(d) for d in sliced_opts))
                line_parts.append("   ".join(block_cells))
            line_str = " | ".join(line_parts)

            if line_idx in (2, 5, 11, 14, 20, 23):
                line_str = line_str + "\n"

            lines.append(line_str)

            if line_idx in (8, 17):
                lines.append("----------------------|-----------------------|----------------------")

        return "\n".join(lines)

    def load_from_json(self, filename):
        print(f"Reading from file: {filename}")
        with open(filename, 'r') as f:
            data = json.load(f)

        if len(data) != 9 or any(len(row) != 9 for row in data):
            raise ValueError("Board must be a 9x9 grid")

        for row in range(9):
            for col in range(9):
                val = data[row][col]
                if val is not None:
                    self.grid[row][col].collapse(val)
                    self.propagate(row, col)
                    self.solved_cells += 1

    def propagate(self, row, col):
        val = self.grid[row][col].collapsed_value

        # Remove from row
        for c in range(9):
            if c != col:
                self.grid[row][c].remove_option(val)

        # Remove from column
        for r in range(9):
            if r != row:
                self.grid[r][col].remove_option(val)

        # Remove from 3x3 block
        block_row = (row // 3) * 3
        block_col = (col // 3) * 3
        for r in range(block_row, block_row + 3):
            for c in range(block_col, block_col + 3):
                if r != row or c != col:
                    self.grid[r][c].remove_option(val)

    def solve(self):
        if self.solved_cells == 81:
            if self.check_solution():
                print("Sudoku solved correctely!")
                return True
            else:
                return False

        # Find all uncollapsed cells with entropy == 1
        entropy_one_cells = [
            (r, c) for r in range(9) for c in range(9)
            if self.grid[r][c].entropy == 1
        ]

        if not entropy_one_cells:
            print("No cells with entropy 1 available — stuck.")
            return False

        # Pick one at random, collapse and propagate
        row, col = random.choice(entropy_one_cells)
        cell = self.grid[row][col]
        value = next(iter(cell.options))

        cell.collapse(value)
        self.solved_cells += 1
        self.propagate(row, col)

        return self.solve()  # Recursive call
    
    def check_solution(self):
        expected_set = set(range(1, 10))

        # Check all cells are collapsed
        for row in range(9):
            for col in range(9):
                cell = self.grid[row][col]
                if not hasattr(cell, 'collapsed_value') or cell.collapsed_value is None:
                    print(f"Cell at ({row},{col}) is not collapsed.")
                    return False

        # Check rows
        for row in range(9):
            values = [self.grid[row][col].collapsed_value for col in range(9)]
            if set(values) != expected_set:
                print(f"Row {row} failed uniqueness check: {values}")
                return False

        # Check columns
        for col in range(9):
            values = [self.grid[row][col].collapsed_value for row in range(9)]
            if set(values) != expected_set:
                print(f"Column {col} failed uniqueness check: {values}")
                return False

        # Check 3x3 subsquares
        for box_row in range(3):
            for box_col in range(3):
                values = []
                for r in range(box_row * 3, box_row * 3 + 3):
                    for c in range(box_col * 3, box_col * 3 + 3):
                        values.append(self.grid[r][c].collapsed_value)
                if set(values) != expected_set:
                    print(f"Subsquare ({box_row},{box_col}) failed uniqueness check: {values}")
                    return False

        return True