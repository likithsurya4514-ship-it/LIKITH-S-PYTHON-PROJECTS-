import random

def rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    print("Rock, Paper, Scissors Game!")
    user = input("Enter your choice: ").lower()
    comp = random.choice(choices)
    print(f"Computer chose: {comp}")

    # Issue: tie condition is broken
    if user == "rock" and comp == "scissors":
        print("You win!")
    elif user == "paper" and comp == "rock":
        print("You win!")
    elif user == "scissors" and comp == "paper":
        print("You win!")
    else:
        print("You lose!")  
