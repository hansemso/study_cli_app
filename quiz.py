import random
study_bank = []


def quiz_mode():

    groups = {}
    
    # Build group dictionary
    for card in study_bank:
        groups.setdefault(card["group"], []).append(card)

    # Shuffle group order
    group_list = list(groups.values())
    random.shuffle(group_list)

    score = 0

    print("\n=== Quiz Mode ===")

    # Iterate groups
    for group in group_list:

        random.shuffle(group)  # shuffle inside group

        for card in group:

            user = input(card["q"] + " ").strip().lower()

            if user.strip().lower() == card["a"].strip().lower():
                print("✔ Correct")
                score += 1
            else:
                print("✘ Wrong (Answer:", card["a"], ")")

    print("\nScore:", score, "/", len(study_bank))


#=========================================

def load_cards():

    try:
        with open("study_cards.txt", "r") as file:
            for line in file:

                if not line.strip():
                    continue

                parts = line.strip().split("|")

                if len(parts) == 4:
                    group_id, card_id, q, a = parts

                    study_bank.append({
                        "group": group_id,
                        "id": card_id,
                        "q": q,
                        "a": a
                    })

    except FileNotFoundError:
        pass

#==========================================

def edit_mode():

    if not study_bank:
        print("No cards available.")
        return

    print("\n=== Edit Mode ===")

    for i, card in enumerate(study_bank):

        print(f"\nProblem {card['group']}{card['id']}")
        print("Q:", card["q"])
        print("A:", card["a"])

        print("\nEdit Options:")
        print("1. Edit Question")
        print("2. Edit Answer")
        print("3. Skip Card")

        choice = input("Select option: ").strip()

        if choice == "1":
            new_q = input("New question (blank = keep): ").strip()
            if new_q:
                card["q"] = new_q

        elif choice == "2":
            new_a = input("New answer (blank = keep): ").strip().lower()
            if new_a:
                card["a"] = new_a

        else:
            continue

    save_all_cards()

    print("\nDone. All edits saved.")

#===============================================

def study_review_session():

    score = 0

    print("\n=== Study Review Session ===")

    for item in study_bank:

        user = input(item["q"] + " ").strip().lower()

        if user.strip().lower() == item["a"].strip().lower():
            print("✔ Correct")
            score += 1
        else:
            print("✘ Wrong (Answer:", item["a"], ")")

    print("\nScore:", score, "/", len(study_bank))

#==============================

def add_study_card():

    print("\n=== Add New Study Card ===")

    group_id = input("Enter card number (e.g. 1,2,3...): ").strip()

    if not group_id.isdigit():
        print("Card number must be a number!")
        return

    card_id = input("Enter card letter (press Enter if none): ").strip()

    if card_id and not card_id.isalpha():
        print("Card sub-ID must be letters only (a,b,c...)")
        return

    # Duplicate check
    for card in study_bank:
        if card.get("group") == group_id and card.get("id") == card_id:
            print("ID already exists!")
            return

    question = input("Enter question: ").strip()
    answer = input("Enter answer: ").strip().lower()

    if not question or not answer:
        print("Invalid input!")
        return

    study_bank.append({
        "group": group_id,
        "id": card_id,
        "q": question,
        "a": answer
    })

    save_all_cards()

    print("Card added!")


#============================================

def save_all_cards():
    with open("study_cards.txt", "w") as file:
        for card in study_bank:
            file.write(
                card.get("group", "").strip() + "|" +
                card.get("id", "").strip() + "|" +
                card.get("q", "").strip() + "|" +
                card.get("a", "").strip() + "\n"
            )

#===================================


def main_menu():

    while True:

        print("\n==== Study CLI App ====")
        print("1. Quiz Mode")
        print("2. Edit Mode")
        print("3. Add Card")
        print("4. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            quiz_mode()

        elif choice == "2":
            edit_mode()

        elif choice == "3":
            add_study_card()

        elif choice == "4":
            break

        else:
            print("Invalid choice")

#=============================================

if __name__ == "__main__":
    load_cards()
    main_menu()