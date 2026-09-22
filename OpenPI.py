import os

# ==========================================
# CONFIG
# ==========================================

OS_NAME = "OpenPI"
VERSION = "1.0"

# ==========================================
# FILESYSTEM
# ==========================================

def fs_ls():
    return os.listdir()

def fs_read(filename):
    with open(filename, "r") as file:
        return file.read()

def fs_write(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def fs_delete(filename):
    os.remove(filename)

def fs_mkdir(dirname):
    os.mkdir(dirname)

def fs_rmdir(dirname):
    os.rmdir(dirname)

def fs_cd(dirname):
    os.chdir(dirname)

def fs_pwd():
    return os.getcwd()

# ==========================================
# COMMANDS
# ==========================================

def cmd_help(args):
    print("Commands:")
    print("  help")
    print("  ls")
    print("  cat <file>")
    print("  write <file>")
    print("  edit <file>")
    print("  rm <file>")
    print("  mkdir <directory>")
    print("  rmdir <directory>")
    print("  cd <directory>")
    print("  pwd")
    print("  echo <text>")
    print("  run <file.py>")
    print("  clear")

def cmd_ls(args):
    files = fs_ls()

    for file in files:
        print(file)

def cmd_cat(args):
    if len(args) == 0:
        print("Usage: cat <file>")
        return

    filename = args[0]

    try:
        content = fs_read(filename)
        print(content)
    except OSError as e:
        print("Error:", e)

def cmd_write(args):
    if len(args) == 0:
        print("Usage: write <file>")
        return

    filename = args[0]

    if filename == "main.py":
        print("Error: main.py is protected by the system.")
        return

    print("Enter the content.")
    print("To finish, enter an empty line.")

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    content = "\n".join(lines)

    try:
        fs_write(filename, content)
        print("File saved:", filename)
    except OSError as e:
        print("Error:", e)

def cmd_edit(args):
    if len(args) == 0:
        print("Usage: edit <file>")
        return

    filename = args[0]

    if filename == "OpenPI.py":
        print("Error: OpenPI.py is protected by the system.")
        return

    try:
        content = fs_read(filename)

        print("Current content:")
        print("----------------")
        print(content)
        print("----------------")
        print("Enter the new content.")
        print("To finish, enter an empty line.")

        lines = []

        while True:
            line = input()

            if line == "":
                break

            lines.append(line)

        new_content = "\n".join(lines)

        fs_write(filename, new_content)

        print("File edited:", filename)

    except OSError as e:
        print("Error:", e)

def cmd_rm(args):
    if len(args) == 0:
        print("Usage: rm <file>")
        return

    filename = args[0]

    if filename == "main.py":
        print("Error: main.py is protected by the system.")
        return

    try:
        fs_delete(filename)
        print("File deleted:", filename)
    except OSError as e:
        print("Error:", e)

def cmd_mkdir(args):
    if len(args) == 0:
        print("Usage: mkdir <directory>")
        return

    dirname = args[0]

    try:
        fs_mkdir(dirname)
        print("Directory created:", dirname)
    except OSError as e:
        print("Error creating directory:", e)

def cmd_rmdir(args):
    if len(args) == 0:
        print("Usage: rmdir <directory>")
        return

    dirname = args[0]

    try:
        fs_rmdir(dirname)
        print("Directory removed:", dirname)
    except OSError as e:
        print("Error removing directory:", e)

def cmd_cd(args):
    if len(args) == 0:
        print("Usage: cd <directory>")
        return

    dirname = args[0]

    try:
        fs_cd(dirname)
    except OSError as e:
        print("Error:", e)

def cmd_pwd(args):
    print(fs_pwd())

def cmd_echo(args):
    print(" ".join(args))

def cmd_run(args):
    if len(args) == 0:
        print("Usage: run <file.py>")
        return

    filename = args[0]

    if not filename.endswith(".py"):
        print("Error: file must be a .py file.")
        return

    try:
        with open(filename, "r") as file:
            code = file.read()

        exec(code, {"__name__": "__main__"})

    except OSError as e:
        print("Error:", e)

    except Exception as e:
        print("Program error:", e)

def cmd_clear(args):
    # ANSI escape sequence to clear the terminal
    print("\033[2J\033[H")

# ==========================================
# COMMAND TABLE
# ==========================================

commands = {
    "help": cmd_help,
    "ls": cmd_ls,
    "cat": cmd_cat,
    "write": cmd_write,
    "edit": cmd_edit,
    "rm": cmd_rm,
    "mkdir": cmd_mkdir,
    "rmdir": cmd_rmdir,
    "cd": cmd_cd,
    "pwd": cmd_pwd,
    "echo": cmd_echo,
    "run": cmd_run,
    "clear": cmd_clear,
}

# ==========================================
# SHELL
# ==========================================

def execute(command):
    parts = command.split()

    if len(parts) == 0:
        return

    name = parts[0]
    args = parts[1:]

    if name in commands:
        commands[name](args)
    else:
        print("Unknown command:", name)

def shell():
    print(OS_NAME, VERSION)
    print("Type 'help' for help.")
    print()

    while True:
        prompt = "OpenPI:" + fs_pwd() + "> "
        command = input(prompt)
        execute(command)

# ==========================================
# BOOT
# ==========================================

def main():
    shell()

main()