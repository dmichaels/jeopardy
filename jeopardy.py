import gzip
import json
import random
import shutil
import re
import sys

# Downloaded this file from (200k_questions.json):
# https://www.kaggle.com/datasets/aravindram11/jeopardy-dataset-updated
#
jeopardy_file = "jeopardy_questions_19840910_20120127.json"
jeopardy_zip_file = "jeopardy_questions_19840910_20120127.json.gz"

def main():

    unzip(jeopardy_zip_file, jeopardy_file)

    with open(jeopardy_file, "r") as f:
        data = json.load(f)

    while True:
        display(data)

def display(data: list[dict]):

    record   = random.choice(data)
    category = record.get("category", "")
    amount   = record.get("value", "")
    answer   = normalize(record.get("question", ""))
    question = normalize(record.get("answer", ""))

    print()
    print(f"Category: {category} > {amount}")
    print(f"Answer:   {answer}")

    input("What Is:  ")
    print(f"\033[F\033[KWhat Is:  {question}")

def normalize(s: str) -> str:
    s = s.strip()
    return re.sub(r"\s+", " ", s.replace("<br />", " ").strip().strip("\"").strip("'").replace("\\'", "'").strip())

def unzip(jeopardy_zip_file: str, jeopardy_file: str) -> str:
    with gzip.open(jeopardy_zip_file, "rb") as fin:
        with open(jeopardy_file, "wb") as fout:
            shutil.copyfileobj(fin, fout)

if __name__ == "__main__":
    main()
