import json
import random
import re
import sys

jeopardy_file = "jeopardy_questions_19840910_20120127.json"

def main():

    with open(jeopardy_file, "r") as f:
        data = json.load(f)

    while True:
        display(data)

def display(data: list[dict]):

    record   = random.choice(data)
    category = record.get('category', '')
    amount   = record.get('value', '')
    answer   = normalize(record.get('question', ''))
    question = normalize(record.get('answer', ''))

    print()
    print(f"Category: {category} | {amount}")
    print(f"Answer:   {answer}")

    input("Question: ")
    print(f"\033[F\033[KQuestion: {question}")

def normalize(s: str) -> str:
    s = s.strip()
    return re.sub(r'\s+', ' ', s.replace("<br />", " ").strip().strip("\"").strip("'").replace("\\'", "'").strip())

if __name__ == "__main__":
    main()
