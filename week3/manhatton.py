#!/usr/bin/env python3
"""
8-Puzzle using A* with Manhattan Distance heuristic
(Pure Python, no extra packages)
Shows cost and all moves with states.
"""

GOAL_STATE = (1,2,3,4,5,6,7,8,0)

# Heuristic: Manhattan Distance
def h_manhattan(state):
    dist = 0
    for i, v in enumerate(state):
        if v != 0:
            goal_r, goal_c = divmod(v-1, 3)
            cur_r, cur_c = divmod(i, 3)
            dist += abs(goal_r - cur_r) + abs(goal_c - cur_c)
    return dist

# Moves
MOVES = {'Up':-3,'Down':3,'Left':-1,'Right':1}

def valid_neighbors(state):
    neighbors = []
    zero_idx = state.index(0)
    zr, zc = divmod(zero_idx, 3)
    for action, delta in MOVES.items():
        new_idx = zero_idx + delta
        if action == 'Left' and zc == 0: continue
        if action == 'Right' and zc == 2: continue
        if action == 'Up' and zr == 0: continue
        if action == 'Down' and zr == 2: continue
        s = list(state)
        s[zero_idx], s[new_idx] = s[new_idx], s[zero_idx]
        neighbors.append((tuple(s), action))
    return neighbors

def is_solvable(state):
    arr = [x for x in state if x != 0]
    inv = sum(1 for i in range(len(arr)) for j in range(i+1,len(arr)) if arr[i]>arr[j])
    return inv % 2 == 0

def pop_min(frontier):
    """Pick and remove the entry with the lowest f."""
    best = min(frontier, key=lambda x: x[0])
    frontier.remove(best)
    return best

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def astar_manhattan(start):
    if not is_solvable(start):
        print("❌ Puzzle not solvable.")
        return

    frontier = []
    g_score = {start:0}
    frontier.append((h_manhattan(start), 0, start, None, None))
    came_from = {start:(None,None)}
    closed = set()

    while frontier:
        f, g, cur, parent, act = pop_min(frontier)
        if parent: 
            came_from[cur] = (parent, act)
        if cur == GOAL_STATE:
            # Reconstruct path
            path, actions = [], []
            s = cur
            while s: 
                p,a = came_from[s]
                path.append(s)
                if a: actions.append(a)
                s = p
            path.reverse(); actions.reverse()

            # Print solution
            print(f"✅ Solution found in {len(actions)} moves (Manhattan Distance)\n")
            for step, (state, move) in enumerate(zip(path, ["Start"]+actions)):
                print(f"Step {step}: Move = {move}, Cost = {step}")
                print_state(state)
            return
        closed.add(cur)
        for neigh,a in valid_neighbors(cur):
            if neigh in closed: continue
            g_new = g_score[cur] + 1
            if neigh not in g_score or g_new < g_score[neigh]:
                g_score[neigh] = g_new
                f_neigh = g_new + h_manhattan(neigh)
                frontier.append((f_neigh, g_new, neigh, cur, a))

if __name__=="__main__":
    # ✅ solvable test cases
    start = (1,2,3,4,5,6,7,0,8)       # easy
    # start = (1,2,3,5,0,6,4,7,8)     # medium
    # start = (8,6,7,2,5,4,3,0,1)     # hard
    astar_manhattan(start)
