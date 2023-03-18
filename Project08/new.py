import heapq


def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader.

    INPUT:
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    for target in to_state:
        index_target = to_state.index(target)
        col_tar = int(index_target/3)
        row_tar = index_target % 3
        if target == 0:
            continue
        else:
            for curr in from_state:
                if curr == target:
                    index_curr = from_state.index(curr)
                    col_cur = int(index_curr/3)
                    row_cur = index_curr % 3
                    distance = distance + abs(col_cur - col_tar)
                    distance = distance + abs(row_cur - row_tar)

    return distance


def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT:
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle.
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT:
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below).
    """
    succ_states = list()
    for i in range(9):
        successors = state.copy()
        if state[i] == 0:
            index_target = i
            if index_target == 0:
                if state[1] != 0:
                    successors[0] = state[1]
                    successors[1] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[3] != 0:
                    successors[0] = state[3]
                    successors[3] = 0
                    succ_states.append(successors)
            elif index_target == 1:
                if state[0] != 0:
                    successors[1] = state[0]
                    successors[0] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[2] != 0:
                    successors[1] = state[2]
                    successors[2] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[4] != 0:
                    successors[1] = state[4]
                    successors[4] = 0
                    succ_states.append(successors)
            elif index_target == 2:
                if state[1] != 0:
                    successors[2] = state[1]
                    successors[1] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[5] != 0:
                    successors[2] = state[5]
                    successors[5] = 0
                    succ_states.append(successors)
            elif index_target == 3:
                if state[0] != 0:
                    successors[3] = state[0]
                    successors[0] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[4] != 0:
                    successors[3] = state[4]
                    successors[4] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[6] != 0:
                    successors[3] = state[6]
                    successors[6] = 0
                    succ_states.append(successors)
            elif index_target == 4:
                if state[1] != 0:
                    successors[4] = state[1]
                    successors[1] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[3] != 0:
                    successors[4] = state[3]
                    successors[3] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[5] != 0:
                    successors[4] = state[5]
                    successors[5] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[7] != 0:
                    successors[4] = state[7]
                    successors[7] = 0
                    succ_states.append(successors)
            elif index_target == 5:
                if state[2] != 0:
                    successors[5] = state[2]
                    successors[2] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[4] != 0:
                    successors[5] = state[4]
                    successors[4] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[8] != 0:
                    successors[5] = state[8]
                    successors[8] = 0
                    succ_states.append(successors)
            elif index_target == 6:
                if state[3] != 0:
                    successors[6] = state[3]
                    successors[3] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[7] != 0:
                    successors[6] = state[7]
                    successors[7] = 0
                    succ_states.append(successors)
            elif index_target == 7:
                if state[4] != 0:
                    successors[7] = state[4]
                    successors[4] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[6] != 0:
                    successors[7] = state[6]
                    successors[6] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[8] != 0:
                    successors[7] = state[8]
                    successors[8] = 0
                    succ_states.append(successors)
            elif index_target == 8:
                if state[5] != 0:
                    successors[8] = state[5]
                    successors[5] = 0
                    succ_states.append(successors)
                    successors = state.copy()
                if state[7] != 0:
                    successors[8] = state[7]
                    successors[7] = 0
                    succ_states.append(successors)

    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT:
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    pq = []  # open
    closed = []
    set = []
    dis = get_manhattan_distance(state, goal_state)
    heapq.heappush(pq, (dis, state, (0, dis, -1)))
    while len(pq) != 0:
        n = heapq.heappop(pq)  # temporary node
        state = n[1]
        closed.append(state)
        set.append(n[2][2])
        parent = closed.index(state)
        if state == goal_state:
            pq.append(n)  # it should be checked when successor were generated so add it back when check it
            break
        succ = get_succ(state)
        for node in succ:
            if closed.__contains__(node):
                continue
            dis = get_manhattan_distance(node, goal_state)
            heapq.heappush(pq, (n[2][0] + dis + 1, node, (n[2][0]+1, dis, parent)))

    parent = n[2][2]
    move = n[2][0]
    trace = [[state, n[2][1], move]]
    while move != 0:
        state = closed[parent]
        parent = set[parent]
        dis = get_manhattan_distance(state, goal_state)
        move = move - 1
        trace.append([state, dis, move])
    trace.reverse()
    for tb in trace:
        print(str(tb[0]) + " h = " + str(tb[1]) + " moves: " + str(tb[2]))
    print("Max queue length: " + str(len(pq)))

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1,2,3,4,5,6,7,0,0]))
    print()

    solve([4, 3, 0, 5, 1, 6, 7, 2, 0])
    print()