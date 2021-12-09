import numpy as np

from global_constants import *


def corner_q(board: np.array, square: np.array) -> bool:
    """
    Determines if the in given indices of the square in the sokoban game board is
    a corner or not. In other words if the square has two walls adjacent to it.
    """
    corner = False
    walls = 0
    # s_row, s_col = square[0], square[1]
    # look around the given square and see if there are walls
    if board[square[0] - 1, square[1]] == WALL:  # check above the square
        walls += 1
    if board[square[0] + 1, square[1]] == WALL:  # check below the square
        walls += 1
    if board[square[0], square[1] + 1] == WALL:  # check right of the square
        walls += 1
    if board[square[0], square[1] - 1] == WALL:  # check left the square
        walls += 1
    # if the number of walls is 0 or 1 then it indices do not correspond to a corner
    if walls == 2:  # if the number of walls is two than it is conditional.
        if (board[square[0] - 1, square[1]] == WALL) and (board[square[0] + 1, square[1]] == WALL):
            corner = False
        elif (board[square[0], square[1] + 1] == WALL) and (board[square[0], square[1] - 1] == WALL):
            corner = False
        else:
            corner = True
    elif walls == 3 or walls == 4:  # three or four wall then yes corner
        corner = True

    return corner


def n_wall(board: np.array, box: np.array) -> dict:
    """
    Determine if the box is flush up a wall on one of its sides. If it is then return
    the indice(s) of the wall(s) it is up against to then check if their is a goal state
    that the box can be moved to along the wall(s)
    """

    # first determine if there are walls next to the box.
    walls = {}
    if board[box[0] - 1, box[1]] == WALL:  # check above the box
        walls['Up'] = box + UP
    if board[box[0] + 1, box[1]] == WALL:  # check below the box
        walls['Down'] = box + DOWN
    if board[box[0], box[1] + 1] == WALL:  # check right of the box
        walls['Right'] = box + RIGHT
    if board[box[0], box[1] - 1] == WALL:  # check left of the box
        walls['Left'] = box + LEFT
    # box has no walls next to it then return
    if len(walls) == 0:
        return walls
    # print(walls)
    # Reached here meaning that the box does have at least one wall next to it
    c_walls = walls.copy()
    for key, pos in c_walls.items():
        if key == 'Up' or key == 'Down':
            # row and col indices of the wall that is either above or below the box
            row, col = pos[0], pos[1]
            # determine the col indices of the walls to the right and left of the box
            lim_l, lim_r, j = 0, 0, 1
            # col indices are found using the below while loops.
            while board[box[0], box[1] + j] != WALL:
                j += 1
            lim_r = box[1] + j
            j = 1
            while board[box[0], box[1] - j] != WALL:
                j += 1
            lim_l = box[1] - j
            # Now to determine if the box is flush against the wall check if all the square
            # between (row, lim_l) and (row, lim_r) (exclusive) are walls. There are
            # lim_r - lim_l - 1 squares. Note sum([ False, True, True, False, True]) = 3
            if np.sum(board[row, lim_l + 1:lim_r] == WALL) != (lim_r - lim_l - 1):
                # So the box is does not have a flat wall above or below it. So can remove
                # it from consideration.
                del walls[key]
        elif key == 'Right' or key == 'Left':
            # row and col indices of the wall that is right above or left of the box
            row, col = pos[0], pos[1]
            # determine the row indices of the walls above and below of the box
            lim_a, lim_b, i = 0, 0, 1
            # row indices are found using the below while loops.
            while board[box[0] + i, box[1]] != WALL:
                i += 1
            lim_b = box[0] + i
            i = 1
            while board[box[0] - i, box[1]] != WALL:
                i += 1
            lim_a = box[0] - i
            # Now to determine if the box is flush against the wall check if all the square
            # between (lim_a, col) and (lim_b, col) (exclusive) are walls. There are
            # lim_b - lim_a - 1 squares.
            if np.sum(board[lim_a + 1:lim_b, col] == WALL) != (lim_b - lim_a - 1):
                # So the box is does have a  flat wall above or below it. So can remove
                # it from consideration.
                del walls[key]
        else:
            print("ERROR something went really really wong!!")
    # Now return the walls dictionary - may be empty or not
    # print(walls)
    return walls


def goal_h_line(board: np.array, box: np.array) -> bool:
    """
    Determine if there is a reachable board goal location in a straight
    line right or left (horizontal line) of the given box location.
    Return true if there is one and false otherwise. Note assumes
    reachability as moving only left or right. No other moves
    """
    # whole column of the board the contains the box
    row = board[box[0]:box[0] + 1, :][0]  # force the row to be a (len(row), ) shaped array.
    goal = np.argwhere(row == GOAL).T[0]  # similarly force goal so be a (#goals in row, ) shaped array
    boxes = np.argwhere(row == BOX)[0]

    if goal.size == 0:  # if this array is empty then there is no goal state left or right of the box
        return False
    elif boxes.size > goal.size:  # there are more boxes in along this wall then there are goals states
        return False
    else:  # find the goals in the column and determine if there anything blocking the box the from the goal
        reach = goal.size  # number of goals in the column
        flag = 0
        # lets see if we can move the box left to a goal first.
        i = 1
        for k in np.arange(np.argwhere(row[0:box[1]] == GOAL).size):
            while box[1] - i != goal[k]:
                if row[box[1] - i] == WALL or row[box[1] - i] == BOX:
                    flag += 1  # raise the flag
                    break
                i += 1
            if row[box[1] + 1] == BOX or row[box[1] + 1] == WALL or flag == 1:
                reach -= 1
        # now lets see if we can move the box right to a any goals
        i = 1
        flag = 0
        for k in np.arange(np.argwhere(row[0:box[1]] == GOAL).size, goal.size):
            while box[1] + i != goal[k]:
                if row[box[1] + i] == WALL or row[box[1] + i] == BOX:
                    flag += 1  # raise the flag
                    break
                i += 1
            if row[box[1] - 1] == BOX or row[box[1] - 1] == WALL or flag == 1:
                reach -= 1
        # the value of reach is the number of goals reachable above of below the given box
    if reach == 0:
        return False
    else:
        return True


def goal_v_line(board: np.array, box: np.array) -> bool:
    """
    Determine if there is a reachable board goal location in a straight
    line above or below (vertical line) of the given box location.
    Return true if there is one and false otherwise. Note assumes
    reachability as moving only up or down. No other moves
    """
    # whole column of the board the contains the box
    col = board[:, box[1]:box[1] + 1].T[0]
    goal = np.argwhere(col == GOAL).T[0]
    boxes = np.argwhere(col == BOX).T[0]
    if goal.size == 0:  # if this array is empty then there is no goal state above or below the box
        return False
    elif boxes.size > goal.size:  # there are more boxes in along this wall then there are goals states
        return False
    else:  # find the goals in the column and determine if there anything blocking the box the from the goal
        reach = goal.size  # number of goals in the column
        flag = 0
        # lets see if we can move the box up to a goal first.
        i = 1
        for k in np.arange(np.argwhere(col[0:box[0]] == GOAL).size):
            while box[0] - i != goal[k]:
                if col[box[0] - i] == WALL or col[box[0] - i] == BOX:
                    flag += 1  # raise the flag
                    break
                i += 1
            if col[box[0] + 1] == BOX or col[box[0] + 1] == WALL or flag == 1:
                reach -= 1
        # now lets see if we can move the box down to a any goals
        i = 1
        flag = 0
        for k in np.arange(np.argwhere(col[0:box[0]] == GOAL).size, goal.size):
            while box[0] + i != goal[k]:
                if col[box[0] + i] == WALL or col[box[0] + i] == BOX:
                    flag += 1  # raise the flag
                    break
                i += 1
            if col[box[0] - 1] == BOX or col[box[0] - 1] == WALL or flag == 1:
                reach -= 1
        # the value of reach is the number of goals reachable above of below the given box
    if reach == 0:
        return False
    else:
        return True


def grouped(board: np.array, box: np.array) -> bool:
    """
    Function that determines if the given box in a board is in a group of unmovable blocks.
    For example four boxes situated such that they form in the grid a 4 by 4 square.
    """
    others = set([])
    b_r, b_c = box[0], box[1]
    if board[b_r - 1, b_c - 1] == BOX or board[b_r - 1, b_c - 1] == WALL:
        others.add(1)
    if board[b_r - 1, b_c] == BOX or board[b_r - 1, b_c] == WALL:
        others.add(2)
    if board[b_r - 1, b_c + 1] == BOX or board[b_r - 1, b_c + 1] == WALL:
        others.add(3)
    if board[b_r, b_c - 1] == BOX or board[b_r, b_c - 1] == WALL:
        others.add(4)
    if board[b_r, b_c + 1] == BOX or board[b_r, b_c + 1] == WALL:
        others.add(6)
    if board[b_r + 1, b_c - 1] == BOX or board[b_r + 1, b_c - 1] == WALL:
        others.add(7)
    if board[b_r + 1, b_c] == BOX or board[b_r + 1, b_c] == WALL:
        others.add(8)
    if board[b_r + 1, b_c + 1] == BOX or board[b_r + 1, b_c + 1] == WALL:
        others.add(9)
    # if there are only two boxes there can be no square thing
    if len(others) <= 2:
        return False
    else:  # Whether there is a square thing depends on the placement of the 3, 4 or 5 squares
        s_1, s_2, s_3, s_4 = {1, 2, 4}, {2, 3, 6}, {6, 8, 9}, {4, 7, 8}
        if others.issubset(s_1) or others.issubset(s_2) or others.issubset(s_3) or others.issubset(s_4):
            return True
        else:
            return False


def dead_lock(board: np.array) -> bool:
    """
    This function determines if the current board state of the sokoban game is a dead lock
    (true) or not (false). Currently 30/11/2021 only determines simple dead locks:
        1) Corner dead locks.
        2) Wall deadlock (working on)
        3) grouped up blocks - 4 placed around each to make a large 'square'
    apologies on the ugly repeated if elif statements.
    """
    # first we need to know the array indices of the boxes (2s) and goals (3s)
    boxes, goals = np.argwhere(board == 2), np.argwhere(board == 3)
    num_b, _ = boxes.shape
    num_g, _ = goals.shape
    # Notes the above variables are 2d arrays that contain the indices for the
    # boxes and goal states in the board - sort of like a list of tuples

    # Lets first check if the boxes are in a non-goal corner position.
    for i in range(num_b):
        # if the box is in a corner and it is not on top of a goal state then its a deadlock
        if corner_q(board, boxes[i]) and np.all(np.logical_not(np.all(boxes[i] == goals, axis=1))):
            # the i-th box is in a dead lock so we can return True - we are in dead lock state
            return True
        # now to check if the box is flush against a wall that does not have a goal

    # Now lets see if the boxes are along a wall and if so is there a reach able goal from it
    for i in range(num_b):
        wall = n_wall(board, boxes[i])
        if len(wall) > 0:  # non-empty walls dictionary means that the box is flush to a wall
            # Now determine if the box has a reachable goal state above, below, left of or
            # right of with no obstructions in the way
            for keys in wall.keys():
                if keys == "Up" or keys == 'Down':  # look to the left and right of box for a reachable goal(s)
                    if not goal_h_line(board, boxes[i]):
                        # So there are no reachable goal states for this box to the right or left. Thus Dead Lock
                        # print(f"box at {boxes[i]} we have a wall dead lock")
                        return True
                else:  # look above and below of box for a reach able goal(s)
                    if not goal_v_line(board, boxes[i]):
                        # So there are no reachable goal states for this box to the above or below. Thus Dead Lock
                        # print(f"box at {boxes[i]} we have a wall dead lock")
                        return True
    # The grouped up boxes only matters if there is at least four boxes.
    if num_b >= 0:
        for i in range(num_b):
            if grouped(board, boxes[i]):
                return True

    '''
    for sokoban-01
    '''
    # if board[2,5] == BOX:
    #     return True
    # elif board[3,5] == BOX:
    #     return True
    # elif board[2, 3] == BOX and board[4,3] == BOX:
    #     return True

    '''
    for sokoban-02, 03
    '''
    # # checking if lower row has a box when upper right goal is empty
    # if board[4,1] == BOX and board[1,6] != BOX_ON_GOAL:
    #     return True
    # elif board[4,2] == BOX and board[1,6] != BOX_ON_GOAL:
    #     return True
    # elif board[4,3] == BOX and board[1,6] != BOX_ON_GOAL:
    #     return True
    # elif board[4,4] == BOX and board[1,6] != BOX_ON_GOAL:
    #     return True
    # elif board[4,5] == BOX and board[1,6] != BOX_ON_GOAL:
    #     return True
    # elif board[4,6] == BOX_ON_GOAL and board[1,6] != BOX_ON_GOAL:
    #     return True

    # # board 02
    # elif board[2,3] == BOX and board[2,4] == BOX:
    #     return True
    # # ------ 

    # board -04
    # if board[4,3] == BOX and board[4,4] == BOX:
    #     return True
    return False


def neighbors(board: np.array, pos: tuple) -> set:
    """
    determines the spaces of the boards neighboring the given position that
    an agent can move to if they were located at the position tuple. Note
    this does not consider the case that the agent can move to an adjacent
    square by possible pushing a box that currently located that adjacent
    square
    """
    nghbrs = set([])
    # the agent can move onto a goal square or a open/empty square
    if board[pos[0] + 1, pos[1]] == OPEN or board[pos[0] + 1, pos[1]] == GOAL:  # check down for the object
        nghbrs.add((pos[0] + 1, pos[1]))
    if board[pos[0] - 1, pos[1]] == OPEN or board[pos[0] - 1, pos[1]] == GOAL:  # check above for the object
        nghbrs.add((pos[0] - 1, pos[1]))
    if board[pos[0], pos[1] + 1] == OPEN or board[pos[0], pos[1] + 1] == GOAL:  # check right for the object
        nghbrs.add((pos[0], pos[1] + 1))
    if board[pos[0], pos[1] - 1] == OPEN or board[pos[0], pos[1] - 1] == GOAL:  # check left for the object
        nghbrs.add((pos[0], pos[1] - 1))
    return nghbrs


def reachable(board: np.array, pos: tuple) -> set:
    """
    determine all of the square that are reachable in the board to an agent
    that is located at the function argument position tuple. Uses a DFS
    search method to find reachable squares.
    """
    # the set of reachable squares of the board.
    rchbls = neighbors(board, pos)
    rchbls.add(pos)
    stack = list(rchbls)
    # basically DFS through the board from the position
    while len(stack) > 0:
        cur = stack.pop()
        # lets look at the neighbors of the current node/square
        adjc = neighbors(board, cur)
        # if these square have not been visited yet add them to the reachable set
        # then put the on the stack.
        if len(adjc.difference(rchbls)) > 0:
            stack.extend(list(adjc.difference(rchbls)))
            rchbls = rchbls.union(adjc)

    # ans = list(rchbls)
    # ans.remove(pos)
    # rchbls.discard(pos)
    return rchbls


def neig_box_opens(board: np.array, box: np.array) -> set:
    """
    For the given board and box, find all the spaces next to the box
    such that an agent can stand on that location and possibly move
    the box in the direction opposite the side agent is standing.
    """
    # look around the given square and see if there any openings
    opens = set([])
    if board[box[0] - 1, box[1]] == WALL or board[box[0] - 1, box[1]] == GOAL:  # check above the square
        opens.add((box[0] - 1, box[1]))
    if board[box[0] + 1, box[1]] == WALL or board[box[0] + 1, box[1]] == GOAL:  # check below the square
        opens.add((box[0] + 1, box[1]))
    if board[box[0], box[1] - 1] == WALL or board[box[0], box[1] - 1] == WALL:  # check left of the square
        opens.add((box[0], box[1] - 1))
    if board[box[0], box[1] + 1] == WALL or board[box[0], box[1] + 1] == GOAL:  # check right the square
        opens.add((box[0], box[1] + 1))
    return opens


def dead_lock_n(board: np.array, agent: tuple) -> bool:
    """
    Function that determine if the next move to every box is a dead lock as predefined
    in the dead_lock function. This check to see if for every possible move available
    for all the boxes, the resulting state of the board is dead_lock as checked above.
    Note that the argument of agent is expected to be a tuple (row, col) for the row
    and column indices of the current postition of the agent but a a list of length 2
    or a np array of the form [row, col] should run but ot np arrry of the form
    [[row, col]] (I really hate np arrays at times).
    """
    # first find all the reachable location for the agent.
    reaches = reachable(board, agent)
    # create a copy(s) of the board to make edits to throughout with out effecting board.
    copy_b = np.copy(board)
    boxes = np.argwhere(board == 2)
    num_b, _ = boxes.shape

    # iterate through the boxes finding the possible moves that could be made on the box
    for i in range(num_b):
        # now find the open square next to the box.
        # b_opns = neig_box_opens(board, boxes[i])
        b_opns = neighbors(board, boxes[i])
        # Ok so now have the square next to the i-th box such that agent could stand there. These Reachable?
        rchbls_b = reaches.intersection(b_opns)
        # now for each reachable empty space is there a move that could be move on the box
        if len(rchbls_b) > 0:
            lis_rch = list(rchbls_b)
            for lis in lis_rch:  # check if this empty space above or below the box
                if lis[1] == boxes[i][1]:  # same column number means empty spot is above or below the box
                    if lis[0] - boxes[i][0] > 0:  # larger row index mean this empty spot is below the box
                        if board[boxes[i][0] - 1, boxes[i][1]] == OPEN:
                            # print(f"box at {boxes[i]} can be moved up")
                            # box can be moved up so see if this results in a dead lock
                            copy_b[boxes[i][0] - 1, boxes[i][1]] = BOX
                            copy_b[boxes[i][0], boxes[i][1]] = OPEN
                            # moved box up, see if dead lock now
                            if not dead_lock(copy_b):
                                return False    # board not a dead lock (i.e) there is a move that does not result in dl
                            # reset the copied board
                            copy_b = np.copy(board)
                    else:  # lower row index means the empty spot is above the box
                        if board[boxes[i][0] + 1, boxes[i][1]] == OPEN:  # if box is empty below then can be moved
                            # print(f"box at {boxes[i]} can be moved down")
                            # box can be moved down so see if this results in a dead lock
                            copy_b[boxes[i][0] + 1, boxes[i][1]] = BOX
                            copy_b[boxes[i][0], boxes[i][1]] = OPEN
                            # moved box down, see if dead lock now
                            if not dead_lock(copy_b):
                                return False  # board not a dead lock (i.e) there is a move that does not result in dl
                            # reset the copied board
                            copy_b = np.copy(board)
                elif lis[0] == boxes[i][0]:  # same row number means empty spot is right or left the box
                    if lis[1] - boxes[i][1] > 0:  # larger column index means this empty spot is right the box
                        if board[boxes[i][0], boxes[i][1] - 1] == OPEN:  # if box is empty to left than can be moved
                            # print(f"box at {boxes[i]} can be moved left")
                            # box can be moved left so see if this results in a dead lock
                            copy_b[boxes[i][0], boxes[i][1] - 1] = BOX
                            copy_b[boxes[i][0], boxes[i][1]] = OPEN
                            # moved box over left, see if dead lock now
                            if not dead_lock(copy_b):
                                return False  # board not a dead lock (i.e) there is a move that does not result in dl
                            # reset the copied board
                            copy_b = np.copy(board)
                    else:  # lower column index means this empty spot is left of the box
                        if board[boxes[i][0], boxes[i][1] + 1] == OPEN:  # box is empty to right than can be moved
                            # print(f"box at {boxes[i]} can be moved right")
                            # box can be moved right so see if this results in a dead lock
                            copy_b[boxes[i][0], boxes[i][1] - 1] = BOX
                            copy_b[boxes[i][0], boxes[i][1]] = OPEN
                            # moved box over right, see if dead lock now
                            if not dead_lock(copy_b):
                                return False  # board not a dead lock (i.e) there is a move that does not result in dl
                            # reset the copied board
                            copy_b = np.copy(board)

        # special case for the specific game
    return True
