#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define INF 100000000
#define N
#define R
#define V
#define C

int *board;
int *col_count;
int *upper_diag_count;
int *lower_diag_count;
int **experimental_conflicts;


int conflicted_count;
int *conflicted_rows;

int conflict_total;
int N;

int place_queen(int new_col, int row){

    //Place
    board[row] = new_col;

    //Modify Counts
    int c = col_count[new_col]++;
    int up = upper_diag_count[new_col + row]++;
    int dn = upper_diag_count[N - new_col + row - 1]++;

    //Modify Total Conflicts - From Going New
    conflict_total += ((c > 1) ? 1 : -1) +
                        ((up >= 2) ? 1: 0) +
                        ((dn >= 1) ? 1 : 0);
}

int move_queen(int new_col, int row){

    //Store Indexs
    int old_col = board[row];

    //Modify Counts
    int c = col_count[old_col]--;
    int up = upper_diag_count[old_col + row]--;
    int dn = lower_diag_count[N - old_col + row - 1]--;

    //Modify Total Conflicts - From Leaving Old 
    conflict_total += ((c >= 1) ? -1: 1) +
                       ((up >= 1) ? -1: 0) +
                        ((dn >= 1) ? -1: 0);

    //Place Queen In Location
    place_queen(new_col, row);

}

int choose_row_to_adjust(n){

    //Linear Approach --------------------------------
    int conflicted_row[];
    int conflicted_count = 0;

    for (int row = 0; row < N; row++){
        col = board[row];

        conflicts = col_count[col] + \
                    upper_diag_count[col + row] + \
                    lower_diag_count[N - col + row - 1]
        if (conflicts){
            conflicted_row[valid_count++] = row;
        }
    }

    return conflicted_rows[rand() % valid_count]
}

int choose_col_to_place(row){

    //Store Lowest, and Col
    int min_conflicts = INF;
    int min_conflict_cols[N];
    int min_conflict_count = 0;
    int up = row;
    int dn = N + row - 1

    //For every Col:
    for (int col = 0; col < N; col++){
        int conflicts = col_count[col] + upper_diag_count[up] + lower_diag_count[dn]
        up += 1;
        dn -= 1;

        //New Lowest
        if (conflicts < min_conflicts){
            min_conflicts = min_conflicts;
            min_conflict_cols[0] = col;
            min_conflict_count = 1;

        //Equal Lowest
        } else if (conflicts == min_conflicts){
            min_conflict_cols[min_conflict_count++] = col;
        }
    }
    //Return A Random Lowest
    return min_conflict_cols[rand() % min_conflict_count];
}

int move(){

    //Conventional----------
    int row = choose_row_within();
    int col = choose_col_to(row);
    move_queen(col, row);

    //Swap-------------------
}
int setup(){

    //RANDOM ROW
    for (int row = 0; row < N; row++){
        int col = rand() % (N + 1);
        place_queen(col, row);
    }

    //GUASSIEN
} 

int main_function(){

    //Setup
    int steps = 0;
    setup();

    //Solve
    while (conflict_total){
        move();
        steps++;
    }
    return steps;
}








int main(int argc, char *argv[]) {

    //Check Arg Count
    if (argc != 5) { printf("Invalid Arg Count\n", argv[0]); return 1;}
    //Store Values
    N = atoi(argv[1]);
    R = atoi(argv[2]);
    V = atoi(argv[3]);
    C = atoi(argv[4]);
    //Check Arg Values
    if (N <= 0 || R <= 0) { printf("Invalid Arg Value\n"); return 1;}

    //srand(42);

    board = malloc(sizeof(int) * N);
    col_count = malloc(sizeof(int) * N);
    upper_diag_count = malloc(sizeof(int) * (2 * N - 1));
    lower_diag_count = malloc(sizeof(int) * (2 * N - 1));

    //experimental_conflicts = malloc(sizeof(int *) * N);

    conflicted_count = 0;
    conflicted_rows = (int *) malloc(N * sizeof(int));


    double total_time_to_solve = 0
    double total_time_to_verify = 0


    for (int i = 0; i < R; i++){

        printf("Running Test %s:", i);

        clock_t start = clock()
        int steps = main_program()
        clock_t end = clock()

        printf(" -- Steps To Solve: %s", steps);

        solve_time = (double)(end - start) / CLOCKS_PER_SEC
        total_time_to_solve += solve_time

        printf(" -- Solved: %s.2f seconds", solve_time);

        //Verify
        if (V){
            clock_t verify_start = clock()
            //VERIFY
            clock_t verify_end = clock()
            verify_time = (double)(verify_end - verify_start) / CLOCKS_PER_SEC
            printf(" -- Verified: %s.2f seconds", verify_time)
        }
    }

    printf("-------------------------------------------------")
    printf("Average Solve: %s.2f s  Average Verify: %s.2f s", 
            total_time_to_solve, total_time_to_verify);
    printf("-------------------------------------------------")

    free(board);
    free(col_count);
    free(upper_diag_count);
    free(lower_diag_count);

    //for (int i = 0; i < N; i++){
    //    free(experimental_conflicts[i])
    //}
    //free(experimental_conflicts)


}