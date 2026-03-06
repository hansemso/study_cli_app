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
# Search Mode
#=====================================================

def search_cards() -> None:
    """Search cards by keyword."""

    if not study_bank:
        print("No cards available.")
        return

    keyword = input("Search keyword: ").strip().lower()

    if not keyword:
        print("Empty keyword.")
        return

    results = [
        card for card in study_bank
        if keyword in card.get("q", "").lower()
        or keyword in card.get("a", "").lower()
    ]

    print(f"\nFound {len(results)} cards\n")

    for card in results:
        print(card.get("q"))
        print("Answer:", card.get("a"))
        print("---")

#====================================================
# Application Entry
#====================================================

def main_menu() -> None:

    while True:

        print("\n==== Study CLI App ====")
        print("1. Quiz Mode")
        print("2. Add Card")
        print("3. Search Cards")
        print("4. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            quiz_mode()

        elif choice == "2":
            add_study_card()

        elif choice == "3":
            search_cards()

        elif choice == "4":
            sys.exit(0)

        else:
            print("Invalid choice")

#====================================================

if __name__ == "__main__":
    load_cards()
    main_menu()