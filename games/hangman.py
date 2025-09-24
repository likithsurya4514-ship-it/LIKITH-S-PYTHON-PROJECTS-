import random

def hangman():
    words = ["cat", "dog", "bat"]  
    word = random.choice(words)
    guessed = []
    tries = 6

    while tries > 0:
        display = "".join([c if c in guessed else "_" for c in word])
        print(display)
        if "_" not in display:
            print("You won!")
            return
        guess = input("Guess a letter: ").lower()
        if guess in guessed:
            print("Already guessed!")
        elif guess in word:
            guessed.append(guess)
        else:
            guessed.append(guess)
            tries -= 1
            print(f"Wrong! Tries left: {tries}")
    print(f"You lost! The word was: {word}")
