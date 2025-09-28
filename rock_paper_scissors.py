import random

def rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    print("Rock, Paper, Scissors Game!")
    user = input("Enter your choice (rock/paper/scissors): ").lower().strip()
    if user not in choices:
        print("Invalid choice. Choose rock, paper, or scissors.")
        return

    comp = random.choice(choices)
    print(f"Computer chose: {comp}")

    if user == comp:
        print("It's a tie!")
    elif (user == "rock" and comp == "scissors") or \
         (user == "paper" and comp == "rock") or \
         (user == "scissors" and comp == "paper"):
        print("You win!")
    else:
        print("You lose!")
