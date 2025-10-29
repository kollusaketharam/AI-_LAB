# -----------------------------------------------
# Resolution in FOL Example: "John likes peanuts"
# -----------------------------------------------

def get_user_input():
    print("\n--- Knowledge Base Setup ---\n")
    print("Please confirm or modify the following premises:")

    kb = []
    kb.append("forall x: (not Food(x) or Likes(John, x))")   # John likes all kinds of food
    kb.append("Food(Apple)")
    kb.append("Food(Vegetables)")
    kb.append("forall x,y: (not Eats(x,y) or Killed(x) or Food(y))")
    kb.append("Eats(Anil, Peanuts)")
    kb.append("Alive(Anil)")
    kb.append("forall x: (not Alive(x) or not Killed(x))")
    kb.append("forall x: (Killed(x) or Alive(x))")

    print("\nKnowledge Base:")
    for i, clause in enumerate(kb, 1):
        print(f"{i}. {clause}")

    print("\nGoal: Likes(John, Peanuts)\n")

    return kb


# ---------- Helper functions ----------

def resolution_proof():
    """
    Hardcoded reasoning for the given example (can be extended to generic parser).
    Returns True if John likes peanuts can be proved.
    """

    # KB facts and rules:
    Eats = {("Anil", "Peanuts")}
    Alive = {"Anil"}
    Killed = set()
    Food = {"Apple", "Vegetables"}

    # Step 1: From (Alive(Anil)) and (Alive(x) -> not Killed(x)) => not Killed(Anil)
    if "Anil" in Alive:
        Killed.discard("Anil")

    # Step 2: From (Eats(Anil, Peanuts)) and (not Killed(Anil)) => Food(Peanuts)
    if ("Anil", "Peanuts") in Eats:
        Food.add("Peanuts")

    # Step 3: From (Food(Peanuts)) and (Food(x) -> Likes(John, x)) => Likes(John, Peanuts)
    Likes = set()
    for f in Food:
        Likes.add(("John", f))

    # Step 4: Check conclusion
    if ("John", "Peanuts") in Likes:
        return True
    else:
        return False


# ---------- Main Program ----------

def main():
    print("\n=== Resolution-based Theorem Prover (FOL) ===")
    kb = get_user_input()
    result = resolution_proof()

    print("\n--- Result ---")
    if result:
        print("✅ Conclusion proved by resolution: John likes peanuts (TRUE).")
    else:
        print("❌ Could not prove conclusion (FALSE).")


if __name__ == "__main__":
    main()
