import random
import time
from collections import defaultdict

# Constants
INF = float('inf')
N = 10000  # Number of queens

def move_queen(col, row):

    global conflict_total

    old_col = board[row]
    old_upper_diag = old_col + row  #experimental_upper_diag[row]
    old_lower_diag = N - old_col + row - 1 # experimental_lower_diag[row]




    col_count[old_col] -= 1
    upper_diag_count[old_upper_diag] -= 1
    lower_diag_count[old_lower_diag] -= 1

    delta1 = 0
    delta1 += -1 if col_count[old_col] >= 1 else 1
    delta1 += -1 if upper_diag_count[old_upper_diag] >= 1 else 0
    delta1 += -1 if lower_diag_count[old_lower_diag] >= 1 else 0
    conflict_total += delta1


    upper_diag =  col + row
    lower_diag = N - col + row - 1

    col_count[col] += 1
    upper_diag_count[upper_diag] += 1
    lower_diag_count[lower_diag] += 1

    delta2 = 0
    delta2 += 1 if col_count[col] > 1 else -1
    delta2 += 1 if upper_diag_count[upper_diag] >= 2 else 0
    delta2 += 1 if lower_diag_count[lower_diag] >= 2 else 0
    conflict_total += delta2

    # Moving To New Position
    board[row] = col


    #TODO: ALL EXPERIMENTAL----------------------------------------
    # experimental_upper_diag[row] = upper_diag
    # experimental_lower_diag[row] = lower_diag

    # print("AT Top Of Move_Queen")

    # updated_conflicts = defaultdict(list)

    # for conflicts, inner in enumerate(experimental_conflicts):

    #     move = []

    #     for iter_row in inner:

    #         if iter_row == row:
    #             after_conflicts =  (col_count[col] 
    #                          + upper_diag_count[col + row] 
    #                          + lower_diag_count[N - col + row - 1] 
    #                          - 3 )

    #             print(f"AFTER: {after_conflicts}")
    #             print(f" DELTAS: {delta1 + delta2}")
                
    #             change = before_conflicts - after_conflicts
                
    #             if change:
    #                 move.append([row, change+1])
    #         else:
    #             iter_col = board[iter_row]
    #             iter_d1 = experimental_upper_diag[iter_row]
    #             iter_d2 = experimental_lower_diag[iter_row]
    #             change = 0
    #             change += (1 if iter_col == col else -1 if iter_col == old_col else 0)
    #             change += (1 if iter_d1 == upper_diag else -1 if iter_d1 == old_upper_diag else 0)
    #             change += (1 if iter_d2 == lower_diag else -1 if iter_d2 == old_lower_diag else 0)

    #             if change:
    #                 move.append([iter_row, change])


    #     for r, c in move:
    #         inner.remove(r)
    #         experimental_conflicts[conflicts + c].add(r)



def move_queen_simple(col, row):
    board[row] = col
    col_count[col] += 1
    upper_diag_count[col + row] += 1
    lower_diag_count[N - col + row - 1] += 1

def setup_board():
    #Counters
    global board, col_count, upper_diag_count, lower_diag_count
    #global experimental_upper_diag, experimental_lower_diag, experimental_conflicts

    board = [-1] * N
    col_count = [0] * N
    upper_diag_count = [0] * (2 * N - 1)
    lower_diag_count = [0] * (2 * N - 1)

    # experimental_upper_diag = [-1] * N
    # experimental_lower_diag = [-1] * N
    # experimental_conflicts = [set() for _ in range(N)]

    #GREEDY ALGORITHM: -------------------------------------------
    col_chosen = random.randint(0, N - 1)
    move_queen_simple(col_chosen, 0)
    for row in range(1, N):
        min_conflict_cols = []
        min_conflicts = INF
        for col in range(N):
            conflicts = col_count[col] + upper_diag_count[col + row] + lower_diag_count[N - col + row - 1]

            if conflicts < min_conflicts:
                min_conflicts = conflicts
                min_conflict_cols = [col]
            elif conflicts == min_conflicts:
                min_conflict_cols.append(col)

        chosen_col = random.choice(min_conflict_cols)
        move_queen_simple(chosen_col, row)

    # #RANDOM -------------------------------------------------------------
    # for row in range(N):
    #     move_queen_simple(random.randint(0, N-1), row)

    # #GUASSIAN------------------------------------------------------------
    # #NOTE: case 1/3 shown, for multiples of 10
    # for j in range(1, N // 2 + 1):
    #     move_queen_simple(j-1, 2*j - 2)
    #     move_queen_simple(N // 2 + j - 1, 2*j - 3)

def get_conflict_total():
    return (sum(abs(x - 1) for x in col_count)) + \
           (sum(max(0, x - 1) for x in upper_diag_count)) + \
           (sum(max(0, x - 1) for x in lower_diag_count))

def setup_experimental():

    #global experimental_upper_diag, experimental_lower_diag, experimental_conflicts

    for row, col in enumerate(board):

        d1 = row + col
        d2 = N - col + row - 1
        experimental_upper_diag[row] = d1
        experimental_lower_diag[row] = d2

        conflicts = col_count[col] + upper_diag_count[d1] + lower_diag_count[d2] - 3

        experimental_conflicts[conflicts].add(row)




def get_most_conflicted_row():

    max_conflicts = -1
    max_conflict_rows = []

    for row, col in enumerate(board):

        conflicts = (
            col_count[col] 
            + upper_diag_count[col + row] 
            + lower_diag_count[N - col + row - 1] 
            - 3  #NOTE: subtract this one for each
        )

        if conflicts > max_conflicts:
            max_conflicts = conflicts
            max_conflict_rows = [row]
        elif conflicts == max_conflicts:
            max_conflict_rows.append(row)

    return random.choice(max_conflict_rows)

def get_least_conflicted_column(row):
    min_conflicts = INF
    min_conflict_cols = []

    for col in range(N):
        conflicts = (
            col_count[col] 
            + upper_diag_count[col + row]
            + lower_diag_count[N- col + row - 1] #NOTE this isnt actually here, so count is conflict
        )

        if conflicts < min_conflicts:
            min_conflicts = conflicts
            min_conflict_cols = [col]
        elif conflicts == min_conflicts:
            min_conflict_cols.append(col)

    return random.choice(min_conflict_cols)






def move():
    row = get_most_conflicted_row()
    col = get_least_conflicted_column(row)
    move_queen(col, row)


def main():

    #Setup
    global conflict_total
    start = time.time()
    steps = 0
    setup_board()
    conflict_total = get_conflict_total()
    #setup_experimental()

    setup = time.time() - start
    print(f"Initialized In: {setup:.2f} conflicts: {conflict_total}")

    #Running
    while(conflict_total):
        move()
        steps += 1

        # if steps % 1 == 0:
        #     print(f"   -{steps}, conflicts {conflict_total}")

    #Timing
    delta = time.time() - start
    print(f" Completed In: {delta:.2f}, in {steps} steps")
    #print(experimental_conflicts)

    return delta

if __name__ == "__main__":
    taken = 0
    for _ in range(1):
        taken += main()
    print("AVERAGE")
    print(taken)