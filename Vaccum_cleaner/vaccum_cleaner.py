def vacuum_cleaner():
    state = {"A": 1, "B": 1}  
    location = "A"
    print("Initial State:", state)

    while 1 in state.values():
        if state[location] == 1:
            print(f"Cleaning Room {location}")
            state[location] = 0
        else:
            print(f"Room {location} already clean")
        location = "B" if location == "A" else "A"

    print("Final State:", state)
    print("All rooms clean ✅")

if __name__ == "__main__":
    vacuum_cleaner()
