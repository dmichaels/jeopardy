import datetime
import json
import random
import re
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "presidents.json")

def main():

    recent_items_max = 20
    recent_items     = []
    data             = {}

    def load():

        nonlocal data

        def non_consecutive_term(item: dict) -> int:
            nonlocal data
            numbers = []
            for record in data:
                if record.get("name") == item.get("name"):
                    numbers.append(record.get("number"))
            if len(numbers) > 1:
                return numbers.index(item.get("number")) + 1
            return 0

        with open(data_file, "r") as f:
            data = json.load(f)
            data.sort(key=lambda value: todate(value["from"]))
            for number, item in enumerate(data, start=1):
                item["number"] = number
            for item in data:
                if (nct := non_consecutive_term(item)) > 0:
                    item["nct"] = nct  # non-consecutive term number
            # print(json.dumps(data, indent=2))
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

    guess_year           = False
    guess_number         = False
    guess_state          = False
    guess_name_by_year   = False
    guess_name_by_number = False
    simple_select        = False

    for arg in sys.argv[1:]:
        arg = arg.lower()
        if arg in ["--year", "-year"]:
            guess_year = True
        elif arg in ["--number", "-number", "--rank", "-rank"]:
            guess_number = True
        elif arg in ["--state", "-state"]:
            guess_state = True
        elif arg in ["--name-by-year", "-name-by-year", "--name", "-name"]:
            guess_name_by_year = True
        elif arg in ["--name-by-number", "-name-by-number", "--name-by-rank", "--name-by-rank"]:
            guess_name_by_number = True
        elif arg in ["--simple", "-simple"]:
            simple_select = True

    if not (guess_number or guess_state or guess_name_by_year or guess_name_by_number):
        guess_year = True

    if guess_name_by_year:
        guess_year         = False
        guess_number         = False
        guess_state        = False
        guess_name_by_number = False

    if guess_name_by_number:
        guess_year         = False
        guess_number         = False
        guess_state        = False
        guess_name_by_year = False

    while True:
        display(select(simple_select), guess_year, guess_number, guess_state, guess_name_by_year, guess_name_by_number)

def display(item: dict, guess_year: bool, guess_number: bool, guess_state: bool,
            guess_name_by_year: bool, guess_name_by_number: bool) -> None:

    guess_simple = guess_year and not (guess_number or guess_state or guess_name_by_year or guess_name_by_number)

    name    = item.get("name", "")
    number  = item.get("number")
    year    = todate(item.get("from")).year
    party   = toparty(item.get("party"))
    home    = item.get("home", "")
    state   = home.split(",")[1].strip()
    nct     = item.get("nct") or 0
    refresh = item.get("__refresh__")

    print()

    if guess_name_by_year:
        print(f"Year:      {year}{' ∆' if refresh else ''}")
        if (answer := normalize(input("President: "))) in name.lower():
            print(f"\033[F\033[KPresident: ✅ RIGHT ⮕  {name}")
        else:
            print(f"\033[F\033[KPresident: ❌ WRONG ⮕> {name}")
        return

    if guess_name_by_number:
        print(f"Number:    {number}{' ∆' if refresh else ''}")
        if (answer := normalize(input("President: "))) in name.lower():
            print(f"\033[F\033[KPresident: ✅ RIGHT ⮕  {name}")
        else:
            print(f"\033[F\033[KPresident: ❌ WRONG ⮕> {name}")
        return

    if nct > 0:
        print(f"President: {name} ({party}) [Term: {nct}]{' ∆' if refresh else ''}")
    else:
        print(f"President: {name} ({party}){' ∆' if refresh else ''}")

    if guess_year:
        if (answer := toint(input("Year:      "))) == year:
            print(f"\033[F\033[KYear:      ✅ RIGHT ⮕  {year}{f' | #{number} | {party} | {home}' if guess_simple else ''}")
        else:
            print(f"\033[F\033[KYear:      ❌ WRONG ⮕> {year}{f' | #{number} | {party} | {home}' if guess_simple else ''}")

    if guess_number:
        if (answer := toint(input("Number:    "))) == number:
            print(f"\033[F\033[KNumber:    ✅ RIGHT ⮕  {number}{f' [{year}]' if not guess_year else ''}")
        else:
            print(f"\033[F\033[KNumber:    ❌ WRONG ⮕> {number}{f' [{year}]' if not guess_year else ''}")

def toint(value: str, fallback: int = 0) -> int:
    try:
        return int(value)
    except ValueError:
        return fallback

def todate(value: str, fallback: datetime.date = datetime.date.min) -> datetime.date:
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except Exception as e:
        return fallback

def toparty(value: str) -> str:
    if value == "Democratic":
        return "D"
    elif value == "Republican":
        return "R"
    elif value == "Federalist":
        return "F"
    elif value == "Democratic-Republican":
        return "D-R"
    elif value == "National Republican":
        return "N-R"
    elif value == "Democratic (Union)":
        return "D-U"
    elif value == "Whig":
        return "W"
    else:
        return value

def normalize(s: str) -> str:
    s = s.strip()
    return re.sub(r"\s+", " ", s.replace("<br />", " ").strip().strip("\"").strip("'").replace("\\'", "'").strip())


if __name__ == "__main__":
    main()
