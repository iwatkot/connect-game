import numpy as np

ROWS, COLS = 6, 7
EMPTY_CELL = "⚪️"
PLAYER1_CELL = "🔴"
PLAYER2_CELL = "🔵"
PLAYER1_WIN = "🟥"
PLAYER2_WIN = "🟦"


def create_board(rows: int, cols: int, empty_cell: str) -> np.ndarray:
    """Creates a new board with the given number of rows and columns filled with the given empty cell.

    :param rows: number of rows
    :type rows: int
    :param cols: number of columns
    :type cols: int
    :param empty_cell: the empty cell value
    :type empty_cell: str
    :return: the new board
    :rtype: np.ndarray
    """
    board = np.full((rows, cols), empty_cell, dtype="<U2")
    return board


def player_turn(board: np.ndarray, player: str) -> bool:
    row, col = check_input(player)
    if board[row][col] != EMPTY_CELL:
        print("This position is already taken, try again!")
        return False
    else:
        board[row][col] = player
        board = apply_gravity(board)
        print("The move was successful!")
        print(board)
        return True


def check_input(player: str) -> tuple[int, int]:
    """Checks if the input is valid and returns the row and column.

    :param player: the player's emoji
    :type player: str
    :return: the row and column
    :rtype: tuple[int, int]
    """
    try:
        row, col = input(
            f"Player {player} enter row between 0 and 5 and column between 0 and 6, separated by a space: "
        ).split()
        row, col = int(row), int(col)
    except ValueError:
        print("Please enter two numbers separated by a space!")
        return check_input(player)
    if not 0 <= row < ROWS or not 0 <= col < COLS:
        print("Row value must be between 0 and 5 and the column between 0 and 6!")
        return check_input(player)
    return row, col


def apply_gravity(board: np.ndarray) -> np.ndarray:
    """Apply gravity to the board, i.e. move all the pieces down.

    :param board: the board to apply gravity to
    :type board: np.ndarray
    :return: the board with gravity applied
    :rtype: np.ndarray
    """
    for col in range(board.shape[1]):
        for row in range(board.shape[0] - 1, -1, -1):
            if board[row][col] == EMPTY_CELL:
                for i in range(row - 1, -1, -1):
                    if board[i][col] != EMPTY_CELL:
                        board[row][col] = board[i][col]
                        board[i][col] = EMPTY_CELL
                        break
    return board


def check_for_game_over(board: np.ndarray) -> bool:
    """Checks if the game is over by finding four consecutive pieces of the same player.
    Tries to find a consecutive sequence with length 4 in all rows, columns and diagonals.

    :param board: the board to check
    :type board: np.ndarray
    :return: True if the game is over, False otherwise
    :rtype: bool
    """
    # Check rows for win.
    for row in range(ROWS):
        for i in range(COLS - 3):
            if (
                board[row][i]
                == board[row][i + 1]
                == board[row][i + 2]
                == board[row][i + 3]
                != EMPTY_CELL
            ):
                win_cells = [(row, i + j) for j in range(4)]
                win_emoji = (
                    PLAYER1_WIN if board[row][i] == PLAYER1_CELL else PLAYER2_WIN
                )
                print(f"Player {win_emoji} won!")
                for cell in win_cells:
                    board[cell] = win_emoji
                return True

    # Check columns for win.
    for col in range(COLS):
        for i in range(ROWS - 3):
            if (
                board[i][col]
                == board[i + 1][col]
                == board[i + 2][col]
                == board[i + 3][col]
                != EMPTY_CELL
            ):
                win_cells = [(i + j, col) for j in range(4)]
                win_emoji = (
                    PLAYER1_WIN if board[i][col] == PLAYER1_CELL else PLAYER2_WIN
                )
                print(f"Player {win_emoji} won!")
                for cell in win_cells:
                    board[cell] = win_emoji
                return True

    # Check top-left to bottom-right diagonals for win.
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if (
                board[i][j]
                == board[i + 1][j + 1]
                == board[i + 2][j + 2]
                == board[i + 3][j + 3]
                != EMPTY_CELL
            ):
                win_cells = [(i + k, j + k) for k in range(4)]
                win_emoji = PLAYER1_WIN if board[i][j] == PLAYER1_CELL else PLAYER2_WIN
                print(f"Player {win_emoji} won!")
                for cell in win_cells:
                    board[cell] = win_emoji
                return True

    # Check top-right to bottom-left diagonals for win.
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if (
                board[i][j]
                == board[i + 1][j - 1]
                == board[i + 2][j - 2]
                == board[i + 3][j - 3]
                != EMPTY_CELL
            ):
                win_cells = [(i + k, j - k) for k in range(4)]
                win_emoji = PLAYER1_WIN if board[i][j] == PLAYER1_CELL else PLAYER2_WIN
                print(f"Player {win_emoji} won!")
                for cell in win_cells:
                    board[cell] = win_emoji
                return True

    return False


if __name__ == "__main__":
    board = create_board(ROWS, COLS, EMPTY_CELL)
    print(f"New game started\n{board}")
    game_over = False
    player = PLAYER1_CELL

    while not game_over:
        if player_turn(board, player):
            player = PLAYER2_CELL if player == PLAYER1_CELL else PLAYER1_CELL
        game_over = check_for_game_over(board)

    print(f"Game over!\n{board}")
