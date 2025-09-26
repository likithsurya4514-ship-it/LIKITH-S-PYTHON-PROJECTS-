import random

def guess_the_number():
    number = random.randint(1, 50)
    attempts = 0
    print("Welcome to Guess the Number! (1-50)")

    while True:
        guess = input("Enter your guess: ")

       
        if not guess.isdigit():
            print("Please enter a valid number!")
            continue

        guess = int(guess)
        attempts += 1
        if guess < number:
            print("Too low!")
        elif guess > number:
            print("Too high!")
        else:
            print(f"Congratulations! You guessed it in {attempts} tries.")
            break
