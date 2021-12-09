from global_constants import *

def is_new_box_on_goal(board, current_num_boxes_on_goals) -> bool:
    new_num_boxes_on_goals = check_box_on_goals(board)
    if current_num_boxes_on_goals < new_num_boxes_on_goals:
        return True
    else:
        return False

def is_box_moved_off_goal(board, current_num_boxes_on_goals) -> bool:
    new_num_boxes_on_goals = check_box_on_goals(board)
    if current_num_boxes_on_goals > new_num_boxes_on_goals:
        return True
    else:
        return False

def is_at_least_one_box_on_goal(board) -> int:
    num_box_on_goals = check_box_on_goals(board)
    if num_box_on_goals >= 1:
        return True
    else:
        return False

def is_all_boxes_on_goals(board, num_goals: int) -> int:
    num_box_on_goals = check_box_on_goals(board)
    if num_box_on_goals == num_goals:
        return True
    else:
        return False

def check_box_on_goals(board) -> int:
    '''
    check if there is a box on goal, and determine exactly how many
    '''
    num_rows = len(board)
    num_cols = len(board[0])

    num_boxes_on_goals = 0

    for m in range(num_rows):
        for n in range(num_cols):
            element = board[m,n]
            if element == BOX_ON_GOAL:
                num_boxes_on_goals += 1
    return num_boxes_on_goals
