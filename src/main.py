import time
from board import Board
from colorama import init, Fore, Style
init(autoreset=True)

if __name__ == "__main__":
    board = Board()

    board.load_from_json("boards/board_2.json")

    start_time = time.time()

    if board.solve():
        end_time = time.time()
        print(board.solution())
        print(Fore.GREEN + f"\nSudoku solved in {end_time - start_time:.4f} seconds.")
    else:
        end_time = time.time()
        print(Fore.RED + "Sudoku not solvable" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Time elapsed: {end_time - start_time:.4f} seconds.")
