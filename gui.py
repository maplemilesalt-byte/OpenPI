import os
import sys
import termios
import tty
import select

RESET = "\033[0m"
REVERSE = "\033[7m"
CLEAR = "\033[2J\033[H"

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        key = sys.stdin.read(1)

        if key == "\033":
            ready, _, _ = select.select([sys.stdin], [], [], 0.05)
            if not ready:
                return "esc"

            second = sys.stdin.read(1)
            if second != "[":
                return "esc"

            third = sys.stdin.read(1)

            return {
                "A": "up",
                "B": "down",
                "C": "right",
                "D": "left",
            }.get(third, "esc")

        if key in ("\r", "\n"):
            return "enter"

        if key == "q":
            return "quit"

        return key

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def draw(files, cursor, cwd):
    print(CLEAR, end="")
    print("OPENPI GUI")
    print("=" * 50)
    print("Path:", cwd)
    print()

    if not files:
        print("  (empty directory)")
    else:
        columns = 4
        for start in range(0, len(files), columns):
            row = files[start:start + columns]

            for i, name in enumerate(row):
                index = start + i
                label = name

                if os.path.isdir(name):
                    label = "[DIR] " + name
                else:
                    label = "[FILE] " + name

                if index == cursor:
                    print(REVERSE + " " + label[:18].ljust(18) + " " + RESET, end="")
                else:
                    print(" " + label[:18].ljust(18) + " ", end="")

            print()

    print()
    print("=" * 50)
    print("ARROWS: move    ENTER: open    Q: quit")
    print("Enter a directory to enter it.")
    print("Enter a .py file to run it.")


def run_file(filename):
    print(CLEAR, end="")
    print("Running:", filename)
    print("=" * 50)

    try:
        with open(filename, "r") as file:
            code = file.read()

        exec(code, {"__name__": "__main__"})

    except Exception as e:
        print()
        print("Program error:", e)

    print()
    print("Press Enter to return to the GUI.")

    while get_key() != "enter":
        pass


def gui():
    cursor = 0

    while True:
        files = sorted(os.listdir())

        if files and cursor >= len(files):
            cursor = len(files) - 1

        draw(files, cursor, os.getcwd())

        key = get_key()

        if key == "quit":
            print(CLEAR, end="")
            return

        if not files:
            continue

        if key == "left":
            cursor = max(0, cursor - 1)

        elif key == "right":
            cursor = min(len(files) - 1, cursor + 1)

        elif key == "up":
            cursor = max(0, cursor - 4)

        elif key == "down":
            cursor = min(len(files) - 1, cursor + 4)

        elif key == "enter":
            selected = files[cursor]

            if os.path.isdir(selected):
                try:
                    os.chdir(selected)
                    cursor = 0
                except OSError as e:
                    print("Error:", e)
            elif selected.endswith(".py"):
                run_file(selected)
            else:
                print(CLEAR, end="")
                print("Selected:", selected)
                print("This file cannot be run by the GUI.")
                print()
                print("Press Enter to return.")

                while get_key() != "enter":
                    pass


if __name__ == "__main__":
    try:
        gui()
    except (KeyboardInterrupt, EOFError):
        print(CLEAR, end="")
