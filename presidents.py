import datetime
import json
import random
import re
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "presidents.json")

def main():

    recent_items_max = 7
    recent_items     = []
    data             = {}

    def load():

        nonlocal data

        def non_consecutive_term(item: dict) -> int:
            nonlocal data
            ranks = []
            for record in data:
                if record.get("name") == item.get("name"):
                    ranks.append(record.get("rank"))
            if len(ranks) > 1:
                return ranks.index(item.get("rank")) + 1
            return 0

        with open(data_file, "r") as f:
            data = json.load(f)
            data.sort(key=lambda value: todate(value["from"]))
            for rank, item in enumerate(data, start=1):
                item["rank"] = rank
            for item in data:
                if (nct := non_consecutive_term(item)) > 0:
                    item["nct"] = nct  # non-consecutive term number
            # print(json.dumps(data, indent=2))
            return data

    def select() -> dict:

        nonlocal recent_items_max, recent_items, data

        ntries_max = 100
        ntries = 1
        while True:
            item = random.choice(data)
            rank = item.get("rank")
            if (rank in recent_items) and (ntries < ntries_max):
                ntries += 1
                continue
            recent_items.append(rank)
            if len(recent_items) > recent_items_max:
                del recent_items[0]
            return item


    data = load()

    guess_year = False
    guess_rank = False
    guess_name = False

    for arg in sys.argv[1:]:
        arg = arg.lower()
        if arg in ["--year", "-year"]:
            guess_year = True
        elif arg in ["--rank", "-rank", "--number", "-number"]:
            guess_rank = True
        elif arg in ["--name", "-name"]:
            guess_name = True

    if not (guess_rank or guess_name):
        guess_year = True
    if guess_name:
        guess_rank = False

    while True:
        display(select(), guess_year, guess_rank, guess_name)

def display(item: dict, guess_year: bool, guess_rank: bool, guess_name: bool = False) -> None:

    rank = item.get("rank")
    name = item.get("name", "")
    year = todate(item.get("from")).year
    nct  = item.get("nct") or 0

    print()

    if guess_name:
        print(f"Number:    {rank}")
        if (answer := normalize(input("President: "))) in name.lower():
            print(f"\033[F\033[KPresident: ✅ RIGHT ⮕  {name}")
        else:
            print(f"\033[F\033[KPresident: ❌ WRONG ⮕> {name}")
    elif nct > 0:
        print(f"President: {name} [Term: {nct}]")
    else:
        print(f"President: {name}")

    if guess_year:
        if (answer := toint(input("Year:      "))) == year:
            print(f"\033[F\033[KYear:      ✅ RIGHT ⮕  {year}{f' [{rank}]' if not guess_rank else ''}")
        else:
            print(f"\033[F\033[KYear:      ❌ WRONG ⮕> {year}{f' [{rank}]' if not guess_rank else ''}")

    if guess_rank:
        if (answer := toint(input("Number:    "))) == rank:
            print(f"\033[F\033[KNumber:    ✅ RIGHT ⮕  {rank}{f' [{year}]' if not guess_year else ''}")
        else:
            print(f"\033[F\033[KNumber:    ❌ WRONG ⮕> {rank}{f' [{year}]' if not guess_year else ''}")

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

def normalize(s: str) -> str:
    s = s.strip()
    return re.sub(r"\s+", " ", s.replace("<br />", " ").strip().strip("\"").strip("'").replace("\\'", "'").strip())


if __name__ == "__main__":
    main()
