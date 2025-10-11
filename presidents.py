import json
import random
import re
import sys

presidents_file = "presidents.json"

def main():

    with open(presidents_file, "r") as f:
        data = json.load(f)

    guess_year = True
    guess_number = True

    if len(sys.argv) > 1:
        if sys.argv[1] == "--year":
            guess_year = True
        elif sys.argv[1] == "--number":
            guess_number = True

    while True:
        display(data, guess_year, guess_number)

def display(data: list[dict], guess_year: bool, guess_number: bool):

    record = random.choice(data)
    number = record.get("number")
    name   = record.get("name", "")
    start  = record.get("start", "")
    term   = find_presidential_multiterm(data, name, start)

    print()
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
