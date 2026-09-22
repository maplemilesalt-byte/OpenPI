import random

print("GUESS")
print("Guess 1-9")

number = random.randint(1, 9)

while True:
    try:
        guess = int(input("> "))

        if guess == number:
            print("You win!")
            break
        elif guess < number:
            print("Higher!")
        else:
            print("Lower!")

    except ValueError:
        print("Numbers only!")
