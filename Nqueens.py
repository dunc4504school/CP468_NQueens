import time

class Nqueens:

    def __init__(self, size, store_solutions=True):

        #The Current State Of Safety In Grid
        self.safety = [[0 for _ in range(size)] for _ in range(size)]

        #Current Attempted Queen Y (index is x)
        self.queens = []

        self.store_solutions = store_solutions


        #Statistics To Store
        self.size = size
        self.solutions = []
        self.solution_count = 0
        self.steps = 0
        self.seconds = time.perf_counter()

        #Solve
        self.solveRecurse(0)

        #Store Time Required
        self.seconds = time.perf_counter() - self.seconds

    def solveRecurse(self, x):

        #Complete Solution
        if x == self.size:
            if self.store_solutions:
                self.solutions.append(self.queens.copy())
            self.solution_count += 1
            return False


        #For Every Y Value
        for y in range(0, self.size):

            #If This Y is safe
            if self.safety[x][y] == 0:

                self.steps += 1

                #Place
                self.modify_safety(x,y,1)

                #If this placement Needs Undoing
                if not self.solveRecurse(x + 1):
                    self.modify_safety(x,y,-1)


        return False

    def modify_safety(self, x, y, delta):

        if delta == 1:
            self.queens.append(y)
        else:
            self.queens.pop()

        #Mark All Further Boxs In Row Not Safe
        for row in range(x, self.size):
            self.safety[row][y] += delta
                
        #Mark All Further Diagonals Not Safe
        for diagonal in range(1, self.size-x):
            if x + diagonal < self.size:
                if y - diagonal >= 0:
                    self.safety[x+diagonal][y-diagonal] += delta

                if y + diagonal < self.size:
                    self.safety[x+diagonal][y+diagonal] += delta


    def output(self):
        return self.size, self.steps, self.seconds, self.solution_count

    def print_solutions(self, clean=False):

        print(f"SIZE: {self.size} HAS {len(self.solutions)} TOTAL SOLUTIONS:")
        for index, solution in enumerate(self.solutions):

            if clean == True:
                print(f"SOLUTION {index}:")
                size = len(solution)
                for y in range(0, size):
                    row = []
                    for x in range(0, size):

                        if solution[x] == y:
                            row.append(1)
                        else:
                            row.append(0)
                    print(row)
            else:
                print(f"SOLUTION {index}:     {solution}")

    