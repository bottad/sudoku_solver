import json
import copy
import time
from colorama import Fore, Style
from utility import clear_console

show_progress = False    # if set updates are shown in the full sudoku
delay = 0.15             # delay in seconds

colors = [
    Fore.GREEN,
    "\033[38;5;46m",   # Bright Green
    "\033[38;5;44m",   # Cyan-Teal
    "\033[38;5;27m",   # Vivid Blue
    Fore.YELLOW,
    "\033[38;5;208m",  # Orange
    "\033[38;5;196m",  # Red
    "\033[38;5;212m",  # Pink
    "\033[38;5;201m",  # Magenta
    "\033[38;5;93m",   # Purple
]

class Cell:
    def __init__(self):
        self.options = set(range(1, 10))
        self.entropy = len(self.options)
        self.collapsed_value = None
        self.guessed = False
        self.guess_idx = 0

    def update_entropy(self):
        if self.entropy != 0:
            options = len(self.options)
            if options > 0:
                self.entropy = options
                return True
            else:
                return False
        else:
            return True

    def remove_option(self, val):
        """Remove a single option from the options set, if it exists."""
        if val in self.options:
            self.options.remove(val)
            if not self.update_entropy():
                return False
        return True

    def collapse(self, val):
        """Set the cell to a fixed value (collapse it)."""
        if val in self.options:
            self.options = {val}
            self.collapsed_value = val
            self.entropy = 0
        else:
            raise ValueError(f"Cannot collapse to {val} because it's not in options")
        
    def guess(self, val):
        """Set the cell to a fixed value (collapse it) and set the guessed flag."""
        if val in self.options:
            self.options = {val}
            self.collapsed_value = val
            self.entropy = 0
            self.guessed = True
        else:
            raise ValueError(f"Cannot collapse to {val} because it's not in options")

    def update_guess_idx(self, guess_idx):
        self.guess_idx = guess_idx

class Board:
    def __init__(self):
        self.grid = [[Cell() for _ in range(9)] for _ in range(9)]
        self.solved_cells = 0
        self.guess_idx = 0

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
                            block_cells.append(f"  {colors[min(cell.guess_idx, len(colors) - 1)]}{cell.collapsed_value}{Style.RESET_ALL}  ")  # 7 chars wide
                            # if cell.guessed:
                            #     block_cells.append(f"  {Fore.YELLOW}{cell.collapsed_value}{Style.RESET_ALL}  ")  # 7 chars wide
                            # else:
                            #     block_cells.append(f"  {Fore.GREEN}{cell.collapsed_value}{Style.RESET_ALL}  ")  # 7 chars wide
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

            lines.append(line_str)

            if line_idx in (2, 5, 11, 14, 20, 23):
                lines.append("                      |                       |                      ")

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
                if not self.grid[row][c].remove_option(val):
                    return False

        # Remove from column
        for r in range(9):
            if r != row:
                if not self.grid[r][col].remove_option(val):
                    return False

        # Remove from 3x3 block
        block_row = (row // 3) * 3
        block_col = (col // 3) * 3
        for r in range(block_row, block_row + 3):
            for c in range(block_col, block_col + 3):
                if r != row or c != col:
                    if not self.grid[r][c].remove_option(val):
                        return False

        return True

    def solve(self):
        if show_progress:
            print(self)
            if delay == 0.0:
                input()
            else:
                time.sleep(delay)
            clear_console()

        if self.solved_cells == 81:
            if self.check_solution():
                # print("Sudoku solved correctly!")
                return True
            else:
                print(f"{Fore.RED}Solution is invalid.{Style.RESET_ALL}")
                return False

        # Find all uncollapsed cells with entropy == 1
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                if cell.entropy == 1:
                    value = next(iter(cell.options))
                    cell.collapse(value)
                    cell.update_guess_idx(self.guess_idx)
                    self.solved_cells += 1
                    if not self.propagate(r, c):
                        return False
                    return self.solve()  # Recursive call

        for target_entropy in range(2, 10):  # Try entropy 2 to 9
            for r in range(9):
                for c in range(9):
                    cell = self.grid[r][c]
                    if cell.entropy == target_entropy:
                        for guess in list(cell.options):
                            if show_progress:
                                print(f"Guessing {guess} at ({r}, {c}) with entropy {target_entropy} and guess index {self.guess_idx + 1}\n")
                            board_copy = copy.deepcopy(self)
                            board_copy.guess_idx += 1

                            board_copy.grid[r][c].guess(guess)
                            board_copy.grid[r][c].update_guess_idx(board_copy.guess_idx)
                            board_copy.solved_cells += 1
                            board_copy.propagate(r, c)
                            if board_copy.solve():
                                self.grid = board_copy.grid
                                self.solved_cells = board_copy.solved_cells
                                return True
                            elif show_progress:
                                print(f"Backtracking from guess {guess} at ({r}, {c})")
                        return False  # No valid guess worked for this cell

        print("Stuck — no cell with entropy 1-9 left!")
        return False
    
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
    
    def solution(self):
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

            lines.append(line_str)

            if line_idx in (2, 5, 11, 14, 20, 23):
                lines.append("                      |                       |                      ")

            if line_idx in (8, 17):
                lines.append("----------------------|-----------------------|----------------------")

        lines.append(f"{Fore.GREEN}Green{Style.RESET_ALL} numbers were unique, {Fore.YELLOW}yellow{Style.RESET_ALL} numbers had to be guessed.{Style.RESET_ALL}")

        return "\n".join(lines)
