import json
import random
import re
import os
import sys
import unicodedata

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "countries.json")

def main():


    def load(capitals: bool = False, include_islands: bool = True, include_non_islands: bool = True) -> dict:
        with open(data_file, "r") as f:
            data = json.load(f)
            data.sort(key=lambda value: value["capital"] if capitals else value["country"], reverse=False)
            if not include_islands:
                data = [item for item in data if not item["is_small_island"]]
            if not include_non_islands:
                data = [item for item in data if item["is_small_island"]]
            for number, item in enumerate(data, start=1):
                item["number"] = number
                item["country_normalized"] = normalize_name(item["country"])
                item["capital_normalized"] = normalize_name(item["capital"])
            return data

    def select(data: dict) -> dict:

        recent_item_max = 20

        recent_item_numbers_variable_name = f"recent_item_numbers{id(data)}"
        if not hasattr(select, recent_item_numbers_variable_name):
            setattr(select, recent_item_numbers_variable_name, [])
        recent_item_numbers = getattr(select, recent_item_numbers_variable_name)

        data_local_variable_name = f"data_{id(data)}"
        if not hasattr(select, data_local_variable_name):
            setattr(select, data_local_variable_name, data_local := data.copy())
        data_local = getattr(select, data_local_variable_name)

        ntries_max = 100
        ntries = 1
        while True:
            item = random.choice(data_local)
            data_local.remove(item)
            if not data_local:
                setattr(select, data_local_variable_name, data_local := data.copy())
            number = item.get("number")
            if (number in recent_item_numbers) and (ntries < ntries_max):
                ntries += 1
                data_local.append(item)
                continue
            recent_item_numbers.append(number)
            if len(recent_item_numbers) > recent_item_max:
                del recent_item_numbers[0]
            item["__refresh__"] = (len(data_local) == len(data) - 1)
            return item

    option_islands = False
    option_noislands = False
    option_capitals = False
    option_dump = False

    for arg in sys.argv[1:]:
        arg = arg.lower()
        if arg in ["--islands", "-islands", "--island", "-island"]:
            option_islands = True
        elif arg in ["--noislands", "-noislands", "--noisland", "-noisland"]:
            option_noislands = True
        elif arg in ["--capitals", "-capitals", "--capital", "-capital"]:
            option_capitals = True
        elif arg in ["--dump", "-dump"]:
            option_dump = True

    include_islands = (option_islands and not option_noislands) or (not option_islands and not option_noislands)
    include_non_islands = (option_noislands and not option_islands) or (not option_islands and not option_noislands)

    data = load(capitals=option_capitals, include_islands=include_islands, include_non_islands=include_non_islands)

    if option_dump:
        for number, item in enumerate(data):
            country = item["country"]
            capital = item["capital"]
            if option_capitals:
                print(f"{number + 1:3}. {capital}: {country}")
            else:
                print(f"{number + 1:3}. {country}: {capital}")
        exit(0)

    while True:
        item = select(data)
        country = item.get("country")
        capital = item.get("capital")
        country_normalized = item.get("country_normalized")
        capital_normalized = item.get("capital_normalized")
        refresh = item.get("__refresh__")
        if option_capitals:
            print(f"\nCapital: {capital}{' ∆' if refresh else ''}")
            if (answer := normalize(input("Country: ")).lower()) == country_normalized:
                print(f"\033[F\033[KCountry: ✅ RIGHT ⮕  {country}")
            else:
                print(f"\033[F\033[KCountry: ❌ WRONG ⮕> {country}")
        else:
            print(f"\nCountry: {country}{' ∆' if refresh else ''}")
            if (answer := normalize(input("Capital: ")).lower()) == capital_normalized:
                print(f"\033[F\033[KCapital: ✅ RIGHT ⮕  {capital}")
            else:
                print(f"\033[F\033[KCapital: ❌ WRONG ⮕> {capital}")

def normalize_name(s: str) -> str:
    return remove_accents(normalize(s).replace(".", "").replace(",", "")).replace("-", " ").replace("'", "").lower()

def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().replace("<br />", " ").strip().strip("\"").strip("'").replace("\\'", "'").strip())

def remove_accents(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode("ASCII")

if __name__ == "__main__":
    main()
