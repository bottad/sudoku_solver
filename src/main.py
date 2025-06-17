from board import Board

if __name__ == "__main__":
    board = Board()

    board.load_from_json("boards/board_2.json")

    if board.solve():
        print(board)
