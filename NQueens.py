import random
import time

class NQueens:

    INITIAL_RANDOM = 0
    INITIAL_HALF_DIAGONAL = 1
    INITIAL_ONLY_DIAGONAL = 2
    INITIAL_GREEDY = 3
    INITIAL_GUASSIAN = 4

    CHOICE_HIGHEST = 5
    CHOICE_RANDOM = 6

    MOVEMENT_LEAST = 7
    MOVEMENT_LOWER = 8

    STORING_SUM = 9
    STORING_INCREMENT = 10

    def __init__(self, n,initial, choice, movement, storing, max=100000):


        #Settings
        self.n = n
        self.max = max
        self.initial = initial
        self.choice = choice
        self.movement = movement
        self.storing = storing

        #Builds Board
        self.board = self.generate_initial()

        #Count of Queens In: Row, Col, Diagonals, AntiDiagonals
        self.r_count = [0 for _ in range(self.n)] 
        self.c_count = [0 for _ in range(self.n)]  
        self.d1_count = [0 for _ in range(2*self.n - 1)]
        self.d2_count = [0 for _ in range(2*self.n - 1)]
        self.generate_initial_counts()

    #GOOD
    def generate_initial_counts(self):

        #Counting How Many In Each Row
        for col in range(0,self.n):

            row = self.board[col]
            d1 = self.get_d1(col, row)
            d2 = self.get_d2(col, row)

            self.r_count[row] += 1  
            self.c_count[col] += 1  
            self.d1_count[d1] += 1
            self.d2_count[d2] += 1

        
        #Storing Total Conflicts
        if self.storing == NQueens.STORING_INCREMENT:
            self.conflicts = self.get_total_conflicts()

    #GREAT
    def get_d1(self, col, row):
        return col + row

    #GREAT
    def get_d2(self, col, row):
        return (col - row) + (self.n - 1)

    #(*)   
    def get_conflicts(self, col, row, d1, d2):
        return  abs(self.r_count[row] - 1) + \
                abs(self.c_count[col] - 1) + \
                max(0, self.d1_count[d1] - 1) + \
                max(0, self.d2_count[d2] - 1)

    def get_theoretical_conflicts(self, col, row, d1, d2):
        #NOTE THAT ROW, D1, D2 ARE ONE LOWER (COL IS SAME)
        return  abs(self.r_count[row]) + \
                abs(self.c_count[col] - 1) + \
                max(0, self.d1_count[d1]) + \
                max(0, self.d2_count[d2])

    #(_)
    def is_complete(self):
        if self.storing == NQueens.STORING_SUM:
            return self.get_total_conflicts() == 0
        elif self.storing == NQueens.STORING_INCREMENT:
            return self.conflicts == 0


    #(*) OPTIMIZABLE: Replace With Status Var
    def get_total_conflicts(self):
        return (sum(abs(x - 1) for x in self.c_count)) + \
               (sum(abs(x - 1) for x in self.r_count)) + \
               (sum(max(0, x - 1) for x in self.d1_count)) + \
               (sum(max(0, x - 1) for x in self.d2_count))
        
    
    #(*) OPTIMIZABLE
    def generate_initial(self):
        if self.initial == NQueens.INITIAL_RANDOM:
            return [random.randint(0,self.n-1) for _ in range(self.n)]

        elif self.initial == NQueens.INITIAL_HALF_DIAGONAL:
            return list(range(self.n))
        
        elif self.initial == NQueens.INITIAL_ONLY_DIAGONAL:
            temp =  list(range(self.n))
            random.shuffle(temp)
            return temp

        elif self.initial == NQueens.INITIAL_GREEDY:
            self.board = [-1 for _ in range(self.n)]
            for col in range(self.n):
                print(col)

                # Try to place each queen in a row with the least number of conflicts
                
                min_conflicts = 10000000
                best_row = []
                for row in range(self.n):

                    #self.move_(col, row)

                    conflicts = self.get_total_conflicts()

                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_row = [row]
                    elif conflicts == min_conflicts:
                        best_row.append(row)

                br = random.choice(best_row)

                self.move_firstin_col(col, br)
            return board

        elif self.initial == NQueens.INITIAL_GUASSIAN:

            #NOTE: this approach uses mathematics to ignore algorithm, shouldnt use
            #TODO: implement other 2 cases, if we want to use for anything other then 10^n

            temp = [-1 for _ in range(self.n)]  
    
            if self.n % 2 == 0 and self.n % 6 != 2:
                for j in range(1, self.n // 2 + 1):
                    temp[j - 1] = 2 * j - 2  
                    temp[self.n // 2 + j - 1] = 2 * j - 2 - 1 
                return temp

        else:
            self.board = None
            print("Some Other Board Creation Strategy")

    def generate_choice(self):

        if self.choice == NQueens.CHOICE_HIGHEST:

            max_conflicts = 0
            max_row = []
            for col in range(self.n):

                conflicts = self.get_conflicts(col, self.board[col],
                                   self.get_d1(col, self.board[col]),
                                   self.get_d2(col, self.board[col]))

                if conflicts > max_conflicts:
                    max_conflicts = conflicts
                    max_row = [col]
                elif conflicts == max_conflicts:
                    max_row.append(col)

            max_conflict_column = random.choice(max_row)
            return max_conflict_column

        elif self.choice == NQueens.CHOICE_RANDOM:
            return random.choice([col for col in range(self.n) 
                                         if self.get_conflicts(col, self.board[col],
                                                               self.get_d1(col, self.board[col]),
                                                               self.get_d2(col, self.board[col]))])
 
    def generate_movement(self, col_chosen):

        initial_row = self.board[col_chosen]
        min_conflicts = self.get_conflicts(col_chosen, initial_row, 
                                                self.get_d1(col_chosen, initial_row),
                                                self.get_d2(col_chosen, initial_row))
        min_rows = [initial_row]

        if self.movement == NQueens.MOVEMENT_LEAST:

            d1_iterable = self.get_d1(col_chosen, 0)
            d2_iterable = self.get_d2(col_chosen, 0)
            for try_row in range(0, self.n):

                if try_row == initial_row:
                    pass
                else:
                    theoretical_conflicts = self.get_theoretical_conflicts(col_chosen, try_row, d1_iterable, d2_iterable)
                    
                    #if self.storing == NQueens.STORING_SUM:
                    #    self.move_within_col(col_chosen, try_row)
                    #elif self.storing == NQueens.STORING_INCREMENT:
                    #    self.move(col_chosen, try_row, False)


                    #conflicts = self.get_conflicts(col_chosen, try_row, d1_iterable, d2_iterable)
                    
                    #if theoretical_conflicts - conflicts != 0:
                    #    print("EROR")
                    
                    
                    #If Smaller
                    if theoretical_conflicts < min_conflicts:
                        min_conflicts = theoretical_conflicts
                        min_rows = [try_row]
                    #Equal
                    elif theoretical_conflicts == min_conflicts:
                        min_rows.append(try_row)
                        
                d1_iterable += 1
                d2_iterable -= 1

            #Chose One Of The Smallest Rows (To Avoid Stuck)
            row_chosen = random.choice(min_rows)
          
            if self.storing == NQueens.STORING_SUM:
                self.move_within_col(col_chosen, row_chosen)
            elif self.storing == NQueens.STORING_INCREMENT:
                #self.move(col_chosen, initial_row, False)
                self.move(col_chosen, row_chosen, True)
        
        elif self.movement == NQueens.MOVEMENT_LOWER:

            order = list(range(self.n))
            random.shuffle(order)

            for try_row in order:

                if try_row == initial_row:
                    pass
                else:
                    d1_iterable = self.get_d1(col_chosen, try_row)
                    d2_iterable = self.get_d2(col_chosen, try_row)

                    theoretical_conflicts = self.get_theoretical_conflicts(col_chosen, try_row, d1_iterable, d2_iterable)


                    # if self.storing == NQueens.STORING_SUM:
                    #     self.move_within_col(col_chosen, try_row)
                    # elif self.storing == NQueens.STORING_INCREMENT:
                    #     self.move(col_chosen, try_row, False)

                    #conflicts = self.get_conflicts(col_chosen, try_row, d1_iterable, d2_iterable)

                    if theoretical_conflicts < min_conflicts:
                        min_conflicts = theoretical_conflicts
                        min_rows = [try_row]
                        break
                    elif theoretical_conflicts == min_conflicts:
                        min_rows.append(try_row)

            if self.storing == NQueens.STORING_SUM:
                self.move_within_col(col_chosen, random.choice(min_rows))
            elif self.storing == NQueens.STORING_INCREMENT:
                #self.move(col_chosen, initial_row, False)
                self.move(col_chosen, random.choice(min_rows), True)

    #(*)
    def solve(self):
        remaining = self.max

        while remaining:
            #self.conflicts seems to be increasing more then it should
            #print(f"RUN: {remaining}")
            #print(self.get_total_conflicts() - self.conflicts)
            
            #IF COMPLETE: EXIT
            if self.is_complete():
                return True

            #CHOOSE A COLUMN
            col_chosen = self.generate_choice()

            self.generate_movement(col_chosen)
            
            remaining-=1            

        return False


    # 0: no conflict
    # 1: no conflict
    # 2: conflict

    #sum(max(0, x - 1) for x in self.d1_count)) + \
    #(sum(max(0, x - 1) for x in self.d2_count))

    def move(self, col, row, major):
    
        old = self.board[col]

        if old != -1:
            d1 = self.get_d1(col, old)
            d2 = self.get_d2(col, old)
            self.r_count[old] -= 1
            self.d1_count[d1] -= 1
            self.d2_count[d2] -= 1

            if major:
                self.conflicts += -1 if self.r_count[old] >= 1 else 1

                #AFTER SUBTRACTING: if its one or higher, decrease
                if self.d1_count[d1] >= 1:
                    self.conflicts -= 1
                if self.d2_count[d2] >= 1:
                    self.conflicts -= 1

        d1 = self.get_d1(col, row)
        d2 = self.get_d2(col, row)

        self.r_count[row] += 1
        self.d1_count[d1] += 1
        self.d2_count[d2] += 1

        if major:
            self.conflicts += 1 if self.r_count[row] > 1 else -1
            #AFTER ADDING: if its 2 or more, increase
            if self.d1_count[d1] >= 2:
                self.conflicts += 1
            if self.d2_count[d2] >= 2:
                self.conflicts += 1

        self.board[col] = row



    #NOTE: this applied twice deals with swaps
    def move_within_col(self,col, row):
        old_row = self.board[col]

        self.r_count[old_row] -= 1
        self.d1_count[self.get_d1(col, old_row)] -= 1
        self.d2_count[self.get_d2(col, old_row)] -= 1

        self.move_firstin_col(col, row)
    
    def move_firstin_col(self, col, row):
        self.r_count[row] += 1
        self.d1_count[self.get_d1(col, row)] += 1
        self.d2_count[self.get_d2(col, row)] += 1
        self.board[col] = row


    #GOOD
    def print_board(self, fancy=False):
        if fancy:
            for row in range(self.n):
                line = ""
                for col in range(self.n):
                    if self.board[col] == row:
                        line += "Q "
                    else:
                        line += ". "
                print(line)
                print("\n")
        else:
            print(self.board)

    #GOOD
    def is_valid_solution(config):
        n = len(config)
        for i in range(n):
            for j in range(i+1,n):
                if config[i] == config[j] or abs(config[i] - config[j]) == j - i:
                    return False
        return True


