import json
import subprocess
import tempfile
import shutil

start = int(input("Start ID: "))
end = int(input("End ID: "))

with open("study_cards.json", "r", encoding="utf-8") as f:
    cards = json.load(f)

filtered = []

for card in cards:
    try:
        cid = int(card["id"])
        if start <= cid <= end:
            filtered.append(card)
    except:
        continue

if not filtered:
    print("No cards in that range.")
    exit()

# create temporary deck
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

with open(temp_file.name, "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2)

# backup original
shutil.copy("study_cards.json", "study_cards_backup.json")

# replace deck temporarily
shutil.copy(temp_file.name, "study_cards.json")

try:
    subprocess.run(["python", "quiz.py"])
finally:
    shutil.move("study_cards_backup.json", "study_cards.json")