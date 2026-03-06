import random
import sys
import json
from typing import List, Dict, Any

#====================================================
# Configuration
#====================================================

STORAGE_FILE = "study_cards.json"
study_bank: List[Dict[str, Any]] = []

#====================================================
# Utility Functions
#====================================================

def normalize(text: str | None) -> str:
    """Normalize user input for comparison."""
    return (text or "").strip().lower()


def render_text(text: str | None) -> str:
    """Safely render text fields."""
    return text or ""

#====================================================
# Storage Layer
#====================================================

def load_cards() -> None:
    """Load cards from JSON storage."""

    global study_bank

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                study_bank = data
            else:
                study_bank = []

    except FileNotFoundError:
        study_bank = []

    except json.JSONDecodeError:
        print("Warning: Storage file corrupted. Starting fresh.")
        study_bank = []


def save_all_cards() -> None:
    """Persist cards to JSON storage."""

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(study_bank, f, ensure_ascii=False, indent=2)

#=====================================================
# Quiz Engine
#=====================================================

def quiz_mode() -> None:
    """Run quiz session."""

    if not study_bank:
        print("No cards available.")
        return

    # Group cards by group id
    groups: Dict[str, List[Dict[str, Any]]] = {}

    for card in study_bank:
        groups.setdefault(card.get("group", "0"), []).append(card)

    group_list = list(groups.values())
    random.shuffle(group_list)

    score = 0
    total = len(study_bank)

    print("\n=== Quiz Mode ===")
    print("Press Ctrl+C to exit.\n")

    try:
        for group in group_list:
            random.shuffle(group)

            for card in group:

                question = render_text(card.get("q"))
                answer = card.get("a", "")

                print(question)

                # Multi-answer card support
                if answer and ";" in answer:

                    correct_answers = [normalize(x) for x in answer.split(";")]

                    user_answers = [
                        input("> ")
                        for _ in range(len(correct_answers))
                    ]

                    correct = sum(
                        normalize(u) == c
                        for u, c in zip(user_answers, correct_answers)
                    )

                    if correct == len(correct_answers):
                        print("✔ Correct\n")
                        score += 1
                    else:
                        print(f"✘ Wrong (Answer: {';'.join(correct_answers)})\n")

                # Single answer card
                else:
                    user = input("> ")

                    if normalize(user) == normalize(answer):
                        print("✔ Correct\n")
                        score += 1
                    else:
                        print(f"✘ Wrong (Answer: {answer})\n")

        print(f"\nScore: {score} / {total}")

    except KeyboardInterrupt:
        print(f"\nQuiz terminated. Score: {score} / {total}")

#====================================================
# Card Management
#======================================================

def add_study_card() -> None:
    """Add new study card interactively."""

    print("\n=== Add New Study Card ===")

    group = input("Enter card number (1,2,3...): ").strip()

    if not group.isdigit():
        print("Card number must be numeric.")
        return

    question = multiline_input("Enter question (END to finish):")
    answer = multiline_input("Enter answer (END to finish):")

    if not question or not answer:
        print("Invalid input!")
        return

    # Normalize multi-line answer into semicolon-separated format
    answer = ";".join(
        x.strip().lower()
        for x in answer.split("\n") if x.strip()
    )

    study_bank.append({
        "group": group,
        "q": question.strip(),
        "a": answer
    })

    save_all_cards()
    print("Card added!")

#=====================================================
# Input Helper
#=====================================================

def multiline_input(prompt: str = "Enter text (END to finish):") -> str:
    """Capture multi-line user input."""

    print(prompt)

    lines: List[str] = []

    while True:
        try:
            line = input()

            if line.strip().upper() == "END":
                break

            lines.append(line)

        except EOFError:
            break

    return "\n".join(lines)



#====================================================
# Edit Card
#====================================================

def edit_card() -> None:
    """Edit an existing study card."""

    if not study_bank:
        print("No cards available.")
        return

    print("\n=== Edit Card ===\n")

    # Show card list
    for i, card in enumerate(study_bank, start=1):
        preview = card.get("q", "").split("\n")[0]
        print(f"{i}. {preview}")

    try:
        choice = int(input("\nSelect card number: ").strip())
    except ValueError:
        print("Invalid input.")
        return

    if choice < 1 or choice > len(study_bank):
        print("Card not found.")
        return

    card = study_bank[choice - 1]

    print("\nCurrent Question:\n")
    print(card["q"])

    print("\nCurrent Answer:")
    print(card["a"])

    print("\n1 Edit Question")
    print("2 Edit Answer")
    print("3 Delete Card")
    print("4 Cancel")

    action = input("Select option: ").strip()

    if action == "1":

        new_q = multiline_input("Enter new question (END to finish):")

        if new_q.strip():
            card["q"] = new_q.strip()
            save_all_cards()
            print("Question updated.")

    elif action == "2":

        new_a = multiline_input("Enter new answer (END to finish):")

        if new_a.strip():
            card["a"] = ";".join(
                x.strip().lower()
                for x in new_a.split("\n") if x.strip()
            )

            save_all_cards()
            print("Answer updated.")

    elif action == "3":

        confirm = input("Delete this card? (y/n): ").lower()

        if confirm == "y":
            study_bank.pop(choice - 1)
            save_all_cards()
            print("Card deleted.")

    else:
        print("Cancelled.")


#====================================================
#             MAIN_MENU
#=====================================================

def main_menu() -> None:

    while True:

        print("\n==== Study CLI App ====")
        print("1. Quiz Mode")
        print("2. Add Card")
        print("3. Edit Card")
        print("4. Exit")

        choice = input("Select option: ").strip()

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

#====================================================

if __name__ == "__main__":
    load_cards()
    main_menu()