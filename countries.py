import json
import random
import re
import os
import sys
import unicodedata

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "countries.json")

def main():


    def load():
        with open(data_file, "r") as f:
            data = json.load(f)
            data.sort(key=lambda value: value["country"], reverse=False)
            for number, item in enumerate(data, start=1):
                item["number"] = number
                item["capital_normalized"] = normalize_name(item["capital"])
            return data

    def select(data: dict) -> dict:

        recent_item_max = 20
        recent_item_numbers = []

        if not hasattr(select, "recent_item_numbers"):
            select.recent_item_numbers = []
        data_local_name = f"data_{id(data)}"
        if not hasattr(select, data_local_name):
            setattr(select, data_local_name, data_local := data.copy())
        data_local = getattr(select, data_local_name)

        ntries_max = 100
        ntries = 1
        while True:
            item = random.choice(data_local)
            data_local.remove(item)
            if not data_local:
                setattr(select, data_local_name, data_local := data.copy())
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

    data = load()

    while True:
        item = select(data)
        country = item.get("country")
        capital = item.get("capital")
        capital_normalized = item.get("capital_normalized")
        refresh = item.get("__refresh__")
        print(f"\nCountry: {country}{' ∆' if refresh else ''}")
        if (answer := normalize(input("Capital: ")).lower()) == capital_normalized:
            print()
            print(answer)
            print(capital_normalized)
            print()
            print(f"\033[F\033[KCapital: ✅ RIGHT ⮕  {capital}")
        else:
            print()
            print(answer)
            print(capital_normalized)
            print()
            print(f"\033[F\033[KCapital: ❌ WRONG ⮕> {capital}")

def normalize_name(s: str) -> str:
    return remove_accents(normalize(s).replace(".", "").replace(",", "")).lower()

def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().replace("<br />", " ").strip().strip("\"").strip("'").replace("\\'", "'").strip())

def remove_accents(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode("ASCII")

if __name__ == "__main__":
    main()
