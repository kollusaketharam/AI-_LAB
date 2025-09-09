from collections import deque

goal_state = [[1,2,3],
              [4,5,6],
              [7,8,0]]

moves = [(1,0),(-1,0),(0,1),(0,-1)]

def get_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i,j

def possible_moves(state):
    x,y = get_blank(state)
    for dx,dy in moves:
        nx,ny = x+dx,y+dy
        if 0<=nx<3 and 0<=ny<3:
            new_state = [row[:] for row in state]
            new_state[x][y],new_state[nx][ny] = new_state[nx][ny],new_state[x][y]
            yield new_state

def is_goal(state):
    return state == goal_state

def dfs(state,depth,limit,visited):
    if is_goal(state):
        return [state]
    if depth == limit:
        return None
    visited.add(str(state))
    for nxt in possible_moves(state):
        if str(nxt) not in visited:
            path = dfs(nxt,depth+1,limit,visited)
            if path:
                return [state]+path
    return None

def ids(start):
    limit = 0
    while True:
        visited=set()
        path = dfs(start,0,limit,visited)
        if path:
            return path
        limit+=1

def print_path(path):
    for state in path:
        for row in state:
            print(row)
        print("----")

if __name__=="__main__":
    start_state = [[1,2,3],
                   [4,0,6],
                   [7,5,8]]
    print("DFS (depth=10):")
    res = dfs(start_state,0,10,set())
    if res:
        print_path(res)
    else:
        print("No solution found within depth 10")

    print("\nIDS:")
    res = ids(start_state)
    print_path(res)
