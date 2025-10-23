# JSON data from:
# https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/refs/heads/master/PeriodicTableJSON.json

import datetime
import json
import random
import re
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "periodic_table.json")

def main():

    recent_items_max = 20
    recent_items     = []
    data             = {}

    def load():

        nonlocal data

        with open(data_file, "r") as f:
            data = json.load(f).get("elements")
            data.sort(key=lambda value: toint(value["number"]))
            return data

    def select(simple: bool = True) -> dict:

        nonlocal recent_items_max, recent_items, data

        if not simple:
            if not hasattr(select, "choices"):
                select.choices = data.copy()
            choices = select.choices
        else:
            choices = data

        ntries_max = 100
        ntries = 1
        while True:
            item = random.choice(choices)
            if not simple:
                choices.remove(item) # ; print([element["number"] for element in choices])
                if not choices:
                    choices = select.choices = data.copy()
            number = item.get("number")
            if (number in recent_items) and (ntries < ntries_max):
                ntries += 1
                if not simple:
                    choices.append(item)
                continue
            recent_items.append(number)
            if len(recent_items) > recent_items_max:
                del recent_items[0]
            if not simple:
                item["__refresh__"] = (len(choices) == len(data) - 1)
            return item


    data = load()

    simple_select = False
    guess_number  = True
    guess_name    = False
    dump          = False

    for arg in sys.argv[1:]:
        arg = arg.lower()
        if arg in ["--number", "-number"]:
            guess_number = True
            guess_name = False
        elif arg in ["--name", "-name"]:
            guess_name = True
            guess_number = False
        elif arg in ["--simple", "-simple"]:
            simple_select = True
        elif arg in ["--dump", "-dump"]:
            dump = True
        elif arg.startswith("-"):
            if (max_number := toint(arg[2:] if arg.startswith("--") else arg[1:])) > 0:
                data = data[:max_number]

    if dump:
        longest_name = max(len(item["name"]) for item in data)
        for element in data:
            name = element.get("name")
            number = element.get("number")
            symbol = element.get("symbol")
            category = element.get("category")
            print(f"{name + ':':<{longest_name + 1}} {number:<3} | {symbol:<2} | {category}")
        return

    while True:
        display(select(simple_select), guess_number, guess_name)

def display(item: dict, guess_number: bool, guess_name: bool) -> None:

    name     = item.get("name")
    number   = item.get("number")
    symbol   = item.get("symbol")
    category = item.get("category")
    refresh  = item.get("__refresh__")

    print()

    if guess_name:
        print(f"Number:    {number}")
        if (answer := normalize(input("Name: "))) in name.lower():
            print(f"\033[F\033[KName:   ✅ RIGHT ⮕  {name}")
        else:
            print(f"\033[F\033[KName:   ❌ WRONG ⮕> {name}")
        return

    if guess_number:
        print(f"Name:      {name}{' ∆' if refresh else ''}")
        if (answer := toint(input("Number:    "))) == number:
            print(f"\033[F\033[KNumber:    ✅ RIGHT ⮕  {number} | {symbol} | {category}")
        else:
            print(f"\033[F\033[KNumber:    ❌ WRONG ⮕> {number} | {symbol} | {category}")

def toint(value: str, fallback: int = 0) -> int:
    try:
        return int(value)
    except ValueError:
        return fallback

def normalize(s: str) -> str:
    s = s.strip()
    return re.sub(r"\s+", " ", s.replace("<br />", " ").strip().strip("\"").strip("'").replace("\\'", "'").strip())


if __name__ == "__main__":
    main()
