import os
import sys
import builtins
from termcolor import colored
from pathlib import Path
import subprocess

# 1. Clean ctypes fix to bypass deprecated os.system()
if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7 | 4)

# 2. Force termcolor to active mode inside the binary
os.environ["FORCE_COLOR"] = "1"

# 3. Wrapper to prevent notation glitches in the input() buffer
def colored_input(prompt_text=""):
    builtins.print(prompt_text, end="")
    return builtins.input()
input = colored_input

def warning(prompt): #declare a warning
    print(colored(prompt.upper(),"white","on_red"))


def title(prompt): #Title
    print(colored(str(prompt).upper(),"white","on_green"))     

def see(prompt): #see each file
    print(colored(prompt,"green"))


def subtle(prompt=0):
    print(colored(prompt.upper(),"cyan"))


class Question():
    def __init__(self,prompt,invalid="WRONG ANSWER"):
        self.prompt = prompt
        self.invalid = invalid

    def ask_destination(self):
            path = Path(input(colored(self.prompt,"white","on_blue")))
            print("")
            return path

    def y_or_no(self):
        answers = {'Y': True, 'N': False}
        while True:
            ans = input(colored(self.prompt,"white","on_blue")).upper()
            print("")
            if ans in [*answers]:
                return answers[ans]
            else:
                warning(prompt="INVALID INPUT. (Y/N) ANSWERS ONLY.")
                continue
    
    def scale_setter(self):
        while True:
            try:
                scale = int(input(colored(self.prompt,"white","on_blue")))
                print("")
                return scale
            except ValueError:
                warning(prompt=self.invalid)
                continue

def startfile(filepath):
    if sys.platform == "win32":
        os.startfile(filepath)
    elif sys.platform == "darwin":
        subprocess.call(["open", filepath])
    else:  # Linux / Unix variants
        subprocess.call(["xdg-open", filepath])

