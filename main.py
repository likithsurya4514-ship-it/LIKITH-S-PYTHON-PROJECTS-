from games import guess_the_number, rock_paper_scissors, tic_tac_toe, hangman, snake

def main():
    while True:
        print("\nPython Mini Games")
        print("1. Guess the Number")
        print("2. Rock Paper Scissors")
        print("3. Tic Tac Toe")
        print("4. Hangman")
        print("5. Snake")
        print("6. Exit")
        choice = input("Choose a game: ")

        if choice == "1":
            guess_the_number.guess_the_number()
        elif choice == "2":
            rock_paper_scissors.rock_paper_scissors()
        elif choice == "3":
            tic_tac_toe.tic_tac_toe()
        elif choice == "4":
            hangman.hangman()
        elif choice == "5":
            snake.snake_game()
        elif choice == "6":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
