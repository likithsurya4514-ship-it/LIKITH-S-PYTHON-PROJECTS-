def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def tic_tac_toe():
    board = [[" "]*3 for _ in range(3)]
    player = "X"

    for turn in range(9):
        print_board(board)
        row = int(input("Enter row (0-2): "))
        col = int(input("Enter col (0-2): "))
        if board[row][col] == " ":
            board[row][col] = player
        else:
            print("Spot taken!")
            continue

        # Issue: draw detection missing
        if (board[0][0] == board[0][1] == board[0][2] != " " or
            board[1][0] == board[1][1] == board[1][2] != " " or
            board[2][0] == board[2][1] == board[2][2] != " " or
            board[0][0] == board[1][0] == board[2][0] != " " or
            board[0][1] == board[1][1] == board[2][1] != " " or
            board[0][2] == board[1][2] == board[2][2] != " " or
            board[0][0] == board[1][1] == board[2][2] != " " or
            board[0][2] == board[1][1] == board[2][0] != " "):
            print_board(board)
            print(f"Player {player} wins!")
            return

        player = "O" if player == "X" else "X"
    print_board(board)
    print("Game Over!")  # Issue: no draw message
