import random
import os
import time
import sys

WIDTH = 20
HEIGHT = 10
SPEED = 0.15

def draw(snake, food, score):
    os.system("clear")
    board = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for x, y in snake:
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            board[y][x] = "o"

    head_x, head_y = snake[0]
    board[head_y][head_x] = "@"
    fx, fy = food
    board[fy][fx] = "*"

    print("SNAKE")
    print("+" + "-" * WIDTH + "+")
    for row in board:
        print("|" + "".join(row) + "|")
    print("+" + "-" * WIDTH + "+")
    print("Score:", score)
    print("WASD = move | Q = quit")

def new_food(snake):
    empty = [
        (x, y)
        for y in range(HEIGHT)
        for x in range(WIDTH)
        if (x, y) not in snake
    ]
    return random.choice(empty) if empty else None

def get_key():
    try:
        import select
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            ready, _, _ = select.select([sys.stdin], [], [], SPEED)
            if ready:
                return sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except (ImportError, OSError, AttributeError):
        return None

def game():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (1, 0)
    next_direction = direction
    food = new_food(snake)
    score = 0

    while True:
        key = get_key()

        if key == "q":
            print("\nGame over!")
            return

        if key == "w" and direction != (0, 1):
            next_direction = (0, -1)
        elif key == "s" and direction != (0, -1):
            next_direction = (0, 1)
        elif key == "a" and direction != (1, 0):
            next_direction = (-1, 0)
        elif key == "d" and direction != (-1, 0):
            next_direction = (1, 0)

        direction = next_direction
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake
        ):
            draw(snake, food, score)
            print("\nGame over!")
            return

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = new_food(snake)
            if food is None:
                draw(snake, food, score)
                print("\nYou win!")
                return
        else:
            snake.pop()

        draw(snake, food, score)

if __name__ == "__main__":
    try:
        game()
    except KeyboardInterrupt:
        print("\nGame over!")
