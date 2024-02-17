#!/c/ProgramData/miniconda3/python.exe

import sys
import os
import re

DOCSTRING = '''
    todo <existing id> [del]
    todo <new entry>

    if <existing id> is provided then that todo item is marked as completed
        if the optional del prefix is supplied the item is deleted

    if a <new entry> is provided then that new item is added

    if no args are provided it prints an indexed list of todo items

    to list this help docstring use todo -h or todo --help

'''

TODO_PATH = os.path.join(os.environ["HOME"], ".todo")

COMPLETED = "[completed]"


def print_todo():
    print()
    with open(TODO_PATH) as f:
        lines = f.readlines()
        if len(lines) == 0:
            print("nothing to do :)")
            print()
            print("you can add a new item like so")
            print()
            print("    todo make coffee")
        for n, line in enumerate(lines):
            completed = line.strip().endswith(COMPLETED)
            idx = f"{n}".rjust(2)
            if (completed):
                line = line.strip().replace(COMPLETED, "")
                print(idx, "\033[32m" + line + "✓" + "\033[0m")
            else:
                print(idx, line.strip())


def print_help():
    print(DOCSTRING)

def toggle_complete_entry(id):
    print()
    new_content = []
    with open(TODO_PATH, "r") as f:
        content = f.readlines()
        completed = content[id].strip().endswith(COMPLETED)
        if completed:
            print("un-completing", content[id].strip().replace(COMPLETED, ""))
            new_content = content[0:id] + [content[id].strip().replace(COMPLETED, "") + "\n"] + content[id+1:]
        else:
            print("completing", content[id].strip())
            new_content = content[0:id] + [content[id].strip() + " " + COMPLETED + "\n"] + content[id+1:]

    with open(TODO_PATH, "w") as f:
        f.writelines(new_content)
    print_todo()

def remove_entry(id):
    print()
    new_content = []
    with open(TODO_PATH, "r") as f:
        content = f.readlines()
        print("removing", content[id].strip())
        new_content = content[0:id] + content[id+1:]
    with open(TODO_PATH, "w") as f:
        f.writelines(new_content)
    print_todo()


def add_entry(description):
    print()
    print("adding", description)
    with open(TODO_PATH, "a") as f:
        f.write(f"{description}\n")
    print_todo()


def main():

    args = sys.argv[1:]

    empty = len(args) == 0
    def help(): return args[0] == "-h" or args[0] == "--help"
    def id(): return len(args) == 1 and re.match("^\d+$", args[0])
    def id_del(): return len(args) == 2 and re.match("^\d+$", args[0]) and args[1] == "del"
    def description(): return len(args) >= 1

    if empty:
        print_todo()
    elif help():
        print_help()
    elif id():
        toggle_complete_entry(int(args[0]))
    elif id_del():
        remove_entry(int(args[0]))
    elif description():
        add_entry(" ".join(args))


main()
