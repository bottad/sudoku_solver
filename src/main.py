import time
import os
import argparse

from colorama import init, Fore, Style
init(autoreset=True)

import settings
from board import Board

def parse_arguments():
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument("-n", "--name", nargs='?', help="Name of the Sudoku board (without .json)")
    parser.add_argument("-p", "--show-progress", action="store_true", help="Show solving progress")
    parser.add_argument("-d", "--delay", type=float, default=settings.delay, help="Delay in seconds between updates")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # If no board name provided, prompt the user
    if not args.name:
        args.name = input("Enter the name of the Sudoku board (e.g., board_1): ").strip()

    settings.show_progress = args.show_progress
    settings.delay = args.delay
    board_path = os.path.join("boards", f"{args.name}.json")

    print(f"Main: show:{settings.show_progress}")

    board = Board()

    try:
        board.load_from_json(board_path)
    except FileNotFoundError:
        print(Fore.RED + f"Error: File '{board_path}' not found.")
        exit(1)

    start_time = time.time()

    if board.solve():
        end_time = time.time()
        print(board.solution())
        if settings.show_progress:
            print(Fore.GREEN + "\nSudoku solved correctely.")
        else:
            print(Fore.GREEN + f"\nSudoku solved in {end_time - start_time:.4f} seconds.")
    else:
        end_time = time.time()
        print(Fore.RED + "Sudoku not solvable" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Time elapsed: {end_time - start_time:.4f} seconds.")
