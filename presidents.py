import json
import random
import re
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "presidents.json")

def main():

    with open(data_file, "r") as f:
        data = json.load(f)

    guess_year   = False
    guess_number = False
    guess_name   = False

    for arg in sys.argv[1:]:
        arg = arg.lower()
        if arg in ["--year", "-year"]:
            guess_year = True
        elif arg in ["--number", "-number"]:
            guess_number = True
        elif arg in ["--name", "-name"]:
            guess_name = True

    if not guess_number:
        guess_year = True

    recent_items_max = 12
    recent_items     = []

    while True:
        if (item := display(data, guess_year, guess_number, guess_name)) in recent_items:
            continue
        recent_items.append(item)
        if len(recent_items) >= recent_items_max:
            del recent_items[0]

def display(data: list[dict], guess_year: bool, guess_number: bool, guess_name: bool = False) -> int:

    record = random.choice(data)
    number = record.get("number")
    name   = record.get("name", "")
    start  = record.get("start", "")
    term   = find_presidential_multiterm(data, name, start)

    print()

    if guess_name:
        print(f"Number:    {number}")
        answer = normalize(input("President.... ? "))
        if answer in name.lower():
            print(f"\033[F\033[KPresident: ✅ RIGHT ⮕  {name}")
        else:
            print(f"\033[F\033[KPresident: ❌ WRONG ⮕> {name}")
        return number

    if term > 0:
        print(f"President: {name} (Term: {term})")
    else:
        print(f"President: {name}")

    if guess_year:
        if (answer := input("Year.... ? ")) == start:
            print(f"\033[F\033[KYear:      ✅ RIGHT ⮕  {start}")
        else:
            print(f"\033[F\033[KYear:      ❌ WRONG ⮕> {start}")

    if guess_number:
        if (answer := toint(input("Number.. ? "))) == number:
            print(f"\033[F\033[KNumber:    ✅ RIGHT ⮕  {number}")
        else:
            print(f"\033[F\033[KNumber:    ❌ WRONG ⮕> {number}")

    return number

def toint(value: str, fallback: int = 0) -> int:
    try:
        return int(value)
    except ValueError:
        return fallback

def find_presidential_multiterm(data: list[dict], name: str, start: str) -> int:
    starts = []
    for record in data:
        if record.get("name") == name:
            starts.append(record.get("start"))
    if len(starts) > 1:
        return starts.index(start) + 1
    return 0

def normalize(s: str) -> str:
    s = s.strip()
    return re.sub(r"\s+", " ", s.replace("<br />", " ").strip().strip("\"").strip("'").replace("\\'", "'").strip())


if __name__ == "__main__":
    main()
