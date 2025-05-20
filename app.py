from colorama import Fore, Style, init
import time
import json
import os


r = Fore.LIGHTRED_EX
y = Fore.LIGHTYELLOW_EX
c = Fore.LIGHTCYAN_EX
re = Fore.RESET

dim = Style.DIM
res = Style.RESET_ALL


def style(text_type, strings):
    if text_type == "info":
        pre = f"{c}[*] {re}"
    
    elif text_type == "input":
        pre = f"{y}[+] {re}"
    
    elif text_type == "error":
        pre = f"{r}[!] {re}"

    elif text_type == "count":
        pre = f"{c}{'{:03d}'.format(strings[0])} {re}"


    if len(strings) == 2:
        if text_type == "count":
            string = f"{strings[1]}"
        else:
            string = f"{strings[0]} {dim}{strings[1]}{res}"

    elif len(strings) == 0:
        string = ""

    elif len(strings) == 1:
        if text_type == "input":
            string = f"{y}{strings[0]}{re}"
        else:
            string = strings[0]

    
    output = pre + string

    return output


class Diary():
    def __init__(self):
        self.commands = [
            {
                "name": "new",
                "func": self.new,
                "text": "Creates a new entry"
            },
            {
                "name": "list",
                "func": self.list_all,
                "text": "Lists all entries"
            },
            {
                "name": "help",
                "func": self.show_help,
                "text": "Shows this help"
            },
            {
                "name": "exit",
                "func": self.close,
                "text": "Closes this program"
            },
        ]

        for command in self.commands:
            strings = [
                f"{'{:<7}'.format(command['name'])}", 
                f"{command['text']}"
            ]
            print(style("info", strings))

        self.prompt()


    def prompt(self):
        choose = input(style("input", []))

        not_found = True

        for command in self.commands:
            if choose == command["name"]:
                not_found = False
                command["func"]()

        if not_found:
            strings = [
                f"Command not found."
            ]
            print("")
            print(style("error", strings))
            print("")
            self.prompt()


    def new(self):
        print("")
        
        title = input(style("input", ["Title: "]))
        content = input(style("input", ["Content: "]))
        
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        day = time.strftime("%A")[:3].upper()

        if not os.path.exists("diary.json"):
            with open("diary.json", "w") as file:
                json.dump([], file, indent=4)
            
            print(style("info", ["File successfully created!"]))

        with open("diary.json", "r") as file:
            diary = json.load(file)

        diary.append(
            {
                "title": title,
                "content": content,
                "date": date,
                "day": day
            }
        )

        with open("diary.json", "w") as file:
            json.dump(diary, file, indent=4)

        print(style("info", ["Data successfully written!"]))

        print("")

        self.prompt()

    
    def list_all(self):
        if not os.path.exists("diary.json"):
            print(style("error", "File does not exist."))

        else:
            print("")

            with open("diary.json", "r") as file:
                diary = json.load(file)

            for index, entry in enumerate(diary):
                strings = [
                    index,
                    entry["date"] + " | " +entry["title"]
                ]
                print(style("count", strings))

            print("")

            choose = input(style("input", ["Enter number / q(uit): "]))

            if choose == "q":
                print("")
                self.prompt()

            else:
                try:
                    self.select(diary[int(choose)])
                except Exception:
                    print(style("error", ["There was an error."]))

    
    def select(self, part):
        print("")
        print(f"{dim}Title:   {res}" + part['title'])
        print(f"{dim}Content: {res}" + part['content'])
        print(f"{dim}Date:    {res}" + part['date'])
        print(f"{dim}Day:     {res}" + part['day'])
        print("")

        self.prompt()


    def show_help(self):
        print("")

        for command in self.commands:
            strings = [
                f"{'{:<7}'.format(command['name'])}", 
                f"{command['text']}"
            ]
            print(style("info", strings))

        self.prompt()


    def close(self):
        pass


Diary()