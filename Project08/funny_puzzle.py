import heapq
import numpy as np
import copy


def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    state1 = np.reshape(from_state, (3, 3))
    state2 = np.reshape(to_state, (3, 3))
    distance = 0
    for i in range(3):
        for j in range(3):
            if state1[i][j] == 0:
                continue

            x = int(np.where(state2 == state1[i][j])[0])
            y = int(np.where(state2 == state1[i][j])[1])

            distance = abs(i - x) + abs(j - y) + distance
    return distance


def print_succ(state):
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    succ_states = []

    from_left = [0, 1, 3, 4, 6, 7]
    for i in range(0, 9):
        left = i - 1
        if left in from_left:
            if (state[left] == 0):
                temp = copy.deepcopy(state)
                temp[left] = state[i]
                temp[i] = 0
                if temp not in succ_states and temp != state:
                    succ_states.append(temp)

    from_right = [1, 2, 4, 5, 7, 8]
    for j in range(0, 9):
        right = j + 1
        if right in from_right:
            if (state[right] == 0):
                temp = copy.deepcopy(state)
                temp[right] = state[j]
                temp[j] = 0
                if temp not in succ_states and temp != state:
                    succ_states.append(temp)

    from_top = [0, 1, 2, 3, 4, 5]
    for k in range(0, 9):
        top = k - 3
        if top in from_top:
            if (state[top] == 0):
                temp = copy.deepcopy(state)
                temp[top] = state[k]
                temp[k] = 0
                if temp not in succ_states and temp != state:
                    succ_states.append(temp)

    from_base = [3, 4, 5, 6, 7, 8]
    for l in range(0, 9):
        base = l + 3
        if base in from_base:
            if (state[base] == 0):
                temp = copy.deepcopy(state)
                temp[base] = state[l]
                temp[l] = 0
                if temp not in succ_states and temp != state:
                    succ_states.append(temp)

    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    pq = []
    last = []
    checked = set()
    g = 0
    max_length = 0
    dict_index = 0
    parent_index = -1

    h = get_manhattan_distance(state)
    cost = g + h
    heapq.heappush(pq, (cost, state, (g, h, parent_index), 0))

    while len(pq):
        n = heapq.heappop(pq)
        checked.add(tuple(n[1]))
        if n[1] == goal_state:
            break
        successors = get_succ(n[1])
        g = n[2][0] + 1
        parent_index = n[2][2] + 1
        dict_index += 1

        for successor in successors:
            if tuple(successor) not in checked:
                h = get_manhattan_distance(successor)
                cost = g + h
                heapq.heappush(pq, (cost, successor, (g, h, parent_index), len(last)))
            max_length = max(max_length, len(pq))
            last.append(n)

    trace = []
    parent = len(last) - 1
    while (True):
        trace.insert(0, (n[1], n[2][1]))

        n = last[n[3]]
        if parent == -1:
            break
        parent = n[2][2]

    moves = 0
    for move in trace:
        print(move[0], 'h={} moves: {}'.format(move[1], moves))
        moves += 1
    print(f"Max queue length: {max_length}")

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2, 5, 1, 4, 0, 6, 7, 0, 3])
    print()

    print(get_manhattan_distance([2, 5, 1, 4, 0, 6, 7, 0, 3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([4, 3, 0, 5, 1, 6, 7, 2, 0])
    print()