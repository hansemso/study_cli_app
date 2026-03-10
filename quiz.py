import sys
import json
import os
from typing import List, Dict, Any

# ===============================
# Storage
# ===============================

study_bank: List[Dict[str, Any]] = []

# ===============================
# Utility
# ===============================

def normalize(text: str | None) -> str:
    return (text or "").strip().lower()

# ===============================
# File Storage
# ===============================

def load_cards():

    global study_bank

    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "study_cards.json"
    )

    try:
        with open(path, "r", encoding="utf-8") as f:
            study_bank = json.load(f)

    except:
        study_bank = []

def save_all_cards():

    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "study_cards.json"
    )

    with open(path, "w", encoding="utf-8") as f:
        json.dump(study_bank, f, indent=2, ensure_ascii=False)

# ===============================
# Multiline Input
# ===============================

def multiline_input(prompt="Enter text (END to finish):"):

    print(prompt)

    lines = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    return "\n".join(lines)

# ===============================
# Quiz Mode
# ===============================

def quiz_mode():

    if not study_bank:
        print("No cards available.")
        return

    score = 0
    total = 0

    print("\n=== Quiz Mode ===\n")

    try:

        for card in study_bank:

            print(card.get("code", ""))

            qa_list = card.get("qa", [])  #90

            total += len(qa_list)

            for qa in qa_list:

                print(qa.get("question", ""))

                if normalize(input("> ")) == normalize(qa.get("answer", "")):
                    print("✔ Correct\n")
                    score += 1
                else:
                    print(f"✘ Wrong (Answer: {qa.get('answer','')})\n")

        print(f"\nScore: {score} / {total}")

    except KeyboardInterrupt:
        print(f"\nQuiz terminated. Score: {score} / {total}")

# ===============================
# Add Card
# ===============================

def add_study_card():

    print("\n=== Add New Study Card ===")

    card_id = input("Enter card ID: ").strip()

    if any(card.get("id") == card_id for card in study_bank):
        print("Duplicate ID!")
        return

    code = multiline_input("Enter code (END to finish):")

    qa_list = []

    print("\nEnter QA pairs (END as question to stop)")

    while True:

        q = input("Question: ").strip()

        if q.upper() == "END":
            break

        a = input("Answer: ").strip()

        if q and a:
            qa_list.append({
            "question": q.strip(),
            "answer": a.strip()
        })

    study_bank.append({
        "id": card_id,
        "code": code,
        "qa": qa_list
    })

    save_all_cards()
    print("Card added!")

# ===============================
# Edit Card (Stable Version ⭐)
# ===============================

def edit_card():

    if not study_bank:
        print("No cards available.")
        return

    print("\n=== Edit Card ===\n")

    # Show card list
    for i, card in enumerate(study_bank, start=1):
        print(f"{i}. {card.get('code','').split('\\n')[0]}")

    try:
        choice = int(input("\nSelect card number: ")) - 1
    except:
        print("Invalid input.")
        return

    if choice < 0 or choice >= len(study_bank):
        print("Card not found.")
        return

    card = study_bank[choice]

    print("\n1 Edit Code")
    print("2 Edit QA Answer")
    print("3 Delete Card")
    print("4 Cancel")

    action = input("Select option: ").strip()

    # ======================
    if action == "1":

        new_code = multiline_input("Enter new code (END to finish):")

        if new_code.strip():
            card["code"] = new_code.strip()
            save_all_cards()
            print("Code updated.")

    # ======================
    

    elif action == "2":

        qa_list = card.get("qa", [])

        if not qa_list:
            print("No QA list.")
            return

        print("\nQA List:")

        for i, qa in enumerate(qa_list, start=1):
            print(f"{i}. {qa.get('question','')}")

        try:
            qa_index = int(input("QA number: ").strip()) - 1  # i.e. 'number' of question above to edit.  
        except:
            print("Invalid QA selection.")
            return

        if qa_index < 0 or qa_index >= len(qa_list):
            print("QA not found.")
            return

        print("\nCurrent Answer:")
        print(qa_list[qa_index].get("answer",""))

        new_answer = input("New answer: ").strip()

        if new_answer:
            qa_list[qa_index]["answer"] = new_answer
            card["qa"] = qa_list
            save_all_cards()
            print("Answer updated.")


    # ======================

    elif action == "3":

        if input("Delete card? (y/n): ").lower() == "y":
            study_bank.pop(choice)
            save_all_cards()
            print("Card deleted.")

    else:
        print("Cancelled.")


# ===============================
# Main Menu
# ===============================

def main_menu():

    while True:

        print("\n==== Study CLI App ====")
        print("1. Quiz Mode")
        print("2. Add Card")
        print("3. Edit Card")
        print("4. Exit")

        choice = input("Select option: ")

        if choice == "1":
            quiz_mode()

        elif choice == "2":
            add_study_card()

        elif choice == "3":
            edit_card()

        elif choice == "4":
            sys.exit(0)

        else:
            print("Invalid choice")

# ===============================

if __name__ == "__main__":
    load_cards()
    main_menu()