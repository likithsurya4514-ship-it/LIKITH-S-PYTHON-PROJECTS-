def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board):
    lines = [
        # rows
        (board[0][0], board[0][1], board[0][2]),
        (board[1][0], board[1][1], board[1][2]),
        (board[2][0], board[2][1], board[2][2]),
        # cols
        (board[0][0], board[1][0], board[2][0]),
        (board[0][1], board[1][1], board[2][1]),
        (board[0][2], board[1][2], board[2][2]),
        # diagonals
        (board[0][0], board[1][1], board[2][2]),
        (board[0][2], board[1][1], board[2][0]),
    ]
    for a, b, c in lines:
        if a == b == c and a != " ":
            return a
    return None

def tic_tac_toe():
    board = [[" "]*3 for _ in range(3)]
    player = "X"

    for turn in range(9):
        print_board(board)
        try:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
        except ValueError:
            print("Please enter numbers 0, 1, or 2.")
            continue

        if not (0 <= row <= 2 and 0 <= col <= 2):
            print("Row and column must be 0, 1, or 2.")
            continue

        if board[row][col] == " ":
            board[row][col] = player
        else:
            print("Spot taken!")
            continue

        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            return

        player = "O" if player == "X" else "X"

    print_board(board)
    print("It's a draw!")
