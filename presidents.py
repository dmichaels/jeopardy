import json
import random
import re
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "presidents.json")

def main():

    recent_items_max = 12
    recent_items     = []
    data             = {}

    def load():
        with open(data_file, "r") as f:
            return json.load(f)

    def select() -> tuple[dict, int]:

        nonlocal recent_items_max, recent_items, data

        def multiterm(item: dict) -> int:
            nonlocal data
            starts = []
            for record in data:
                if record.get("name") == item.get("name"):
                    starts.append(record.get("start"))
            if len(starts) > 1:
                return starts.index(item.get("start")) + 1
            return 0

        while True:
            item = random.choice(data)
            number = toint(item.get("number"))
            if number in recent_items:
                continue
            recent_items.append(number)
            if len(recent_items) > recent_items_max:
                del recent_items[0]
            return item, multiterm(item)


    data = load()

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

    if not (guess_number or guess_name):
        guess_year = True
    if guess_name:
        guess_number = False

    while True:
        item, term = select()
        display(item, term, guess_year, guess_number, guess_name)

def display(item: dict, term: int, guess_year: bool, guess_number: bool, guess_name: bool = False) -> None:

    number = toint(item.get("number"))
    name   = item.get("name", "")
    start  = item.get("start", "")

    print()

    if guess_name:
        print(f"Number:    {number}")
        if (answer := normalize(input("President: "))) in name.lower():
            print(f"\033[F\033[KPresident: ✅ RIGHT ⮕  {name}")
        else:
            print(f"\033[F\033[KPresident: ❌ WRONG ⮕> {name}")
    elif term > 0:
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
