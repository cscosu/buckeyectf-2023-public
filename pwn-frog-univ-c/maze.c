#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#define MAZE_DIM	400	/* Number of rows & cols */
#define INNER_DIM	350	/* Number of inner rows & cols */
#define SPAWN_DIM	100 /* Potential spawn rows & cols */

#define SAFE		0
#define FLAG		1
#define FROG		-1
#define NEBULA		-2

#define NUM_PRINTS	8
#define FLAG_SIZE	40

#define UP		'w'
#define LEFT	'a'
#define DOWN	's'
#define RIGHT	'd'

/* Maze cell */
typedef struct cell {
	int x;
	int y;
	struct cell *left;
	struct cell *up;
	struct cell *down;
	struct cell *right;
	int condition;
	int print_flag;
	char contents[FLAG_SIZE];
} cell;

/* Print contents of cell */
void print(char message[], cell *winning_cell) {
	printf("%s: %s\n", message, winning_cell->contents);
}

void print0(cell *winning_cell) {
	print("You shone like a star, here is your flag", winning_cell);
}

void print1(cell *winning_cell) {
	print("*Shines ominously*", winning_cell);
}

void print2(cell *winning_cell) {
	print("You found your place among the nebulas", winning_cell);
}

void print3(cell *winning_cell) {
	print("We nebulas will be watching your progress", winning_cell);
}

void print4(cell *winning_cell) {
	print("Young grasshopper, thank you for braving the frogs", winning_cell);
}

void print5(cell *winning_cell) {
	print("Ribbit, thanks for feeding us with your previous attempts", winning_cell);
}

void print6(cell *winning_cell) {
	print("And so you have satisfied the frogs", winning_cell);
}

void print7(cell *winning_cell) {
	print("You better eat a fly or two", winning_cell);
}

/* Global function array */
void (*g_print_array[NUM_PRINTS])(cell *) = {&print0, &print1, &print2, &print3, &print4, &print5, &print6, &print7};

/* Global const pointing at top left cell */
cell *g_maze;

/* Global pointing current cell */
cell *g_location;

/* Check that cell is not null */
void check_cell_alloc(cell *check) {
	if (check == NULL) {
		perror("cell alloc");
		exit(EXIT_FAILURE);
	}
}

/* Set cell struct values */
void set_cell(cell *current, int x, int y, cell *left, cell *up, cell *down, cell *right, int condition, int print) {
       current->x = x;
       current->y = y;
       current->left = left;
       current->up = up;
       current->down = down;
       current->right = right;
       current->condition = condition;
       current->print_flag = print;
}

void rand_cell_contents(cell *cell_ptr) {
	int i;
	char* flag = cell_ptr->contents;
	for (i=0; i<FLAG_SIZE; i++) {
		flag[i] = 1 + (rand() % 126);
	}
}

/* Allocate 1 cell */
cell *alloc_cell() {
	cell *cell_ptr = (cell *)malloc(sizeof(cell));
	check_cell_alloc(cell_ptr);
	return cell_ptr;
}

/* Allocate 400 * 400 cells */
void allocate_maze() {
	cell *row_ptr, *cell_ptr, *right_ptr, *bottom_ptr;
	int rand_val;
	int x = 0;
	int y = 0;

	/* Seed random with current time */
	srand(time(0));
	
	/* Set maze */
	g_maze = alloc_cell();
	set_cell(g_maze, x, y, NULL, NULL, NULL, NULL, SAFE, rand_val);
	row_ptr = g_maze;
	cell_ptr = g_maze;

	while (y < MAZE_DIM) {
		/* Set a random function */
		rand_val = rand() % NUM_PRINTS;

		/* Allocate adjacent cells */
		if (x+1 != MAZE_DIM) {
			if (y != 0) {
				right_ptr = cell_ptr->up->right->down;
			} else {
				right_ptr = alloc_cell();
			}
			right_ptr->left = cell_ptr;
		} else {
			right_ptr = NULL;
		}

		if (y+1 != MAZE_DIM) {
			bottom_ptr = alloc_cell();
			bottom_ptr->up = cell_ptr;
		} else {
			bottom_ptr = NULL;
		}

		if (x == 0) {
			cell_ptr->left = NULL;
		}

		if (y == 0) {
			cell_ptr->up = NULL;
		}

		/* Set cell position, pointers, and contents */
		set_cell(cell_ptr, x, y, cell_ptr->left, cell_ptr->up, bottom_ptr, right_ptr, SAFE, rand_val);
		rand_cell_contents(cell_ptr);
		x++;
		cell_ptr = cell_ptr->right;

		if (x == MAZE_DIM) {
			x = 0;
			y++;
			row_ptr = row_ptr->down;
			cell_ptr = row_ptr;
		}
	}
}

/* Free 400 * 400 cells */
void de_allocate_maze() {
	cell *cell_ptr = g_maze;
	cell *next_ptr = g_maze;

	/* Go down until null */
	while (cell_ptr->down != NULL) {
		cell_ptr = cell_ptr->down;
	}

	/* Go up until null */
	while (next_ptr != NULL) {
		/* Go right until null */
		while(cell_ptr->right != NULL) {
			cell_ptr = cell_ptr->right;
		}

		next_ptr = cell_ptr->left;

		/* Go left until null */
		while(cell_ptr->left != NULL) {
			next_ptr = cell_ptr->left;
			free(cell_ptr);
			cell_ptr = next_ptr;
		}

		next_ptr = next_ptr->up;
		free(cell_ptr);
		cell_ptr = next_ptr;
	}
}

/* Get cell at a position */
cell *get_cell(int x, int y) {
	cell *loc = g_maze;

	while (loc->x < x) {
		loc = loc->right;
	}

	while (loc->y < y) {
		loc = loc->down;
	}

	return loc;
}

/* Set a random danger */
void set_danger(cell *loc) {
	int danger_val = rand() % 20;

	if (danger_val < 15) {
		loc->condition = FROG;
	} else {
		loc->condition = NEBULA;
	}
}

/* Set dangers "randomly" until get to destination */
cell *rand_rotate(int dest_x, int dest_y, int x_mov, int y_mov, int top, int bot, int left, int right, cell *loc) {
	while (loc->x != dest_x || loc->y != dest_y) {
		int rand_dir = rand() % 4;
		if (rand_dir == 0) {
			if (x_mov >= 0 && loc->x < right) {
				loc = loc->right;
			}
		} else if (rand_dir == 1) {
			if (x_mov <= 0 && loc->x > left) {
				loc = loc->left;
			}
		}else if (rand_dir == 2) {
			if (y_mov <= 0 && loc->y > top) {
				loc = loc->up;
			}
		} else if (rand_dir == 3) {
			if (y_mov >= 0 && loc->y < bot) {
				loc = loc->down;
			}
		}
		
		set_danger(loc);
	}
	
	return loc;
}

/* Create boundary clockwise */
void cw_rotate(int x_left, int x_right, int y_up, int y_down, int pos_x, int pos_y) {
	cell *cell_ptr = get_cell(pos_x, pos_y);
	set_danger(cell_ptr);

	if (pos_x == x_left) {
		if (pos_y == y_up) {
			cell_ptr = rand_rotate(x_right, y_up, 1, 0, y_up, y_up + (y_up + y_down)/20, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_down, 0, 1, y_up, y_down, x_right - (x_left + x_right)/20, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_down, -1, 0, y_down - (y_up + y_down)/20, y_down, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_up, 0, -1, y_up, y_down, x_left, x_left + (x_left + x_right)/20, cell_ptr);
		} else {
			cell_ptr = rand_rotate(x_left, y_up, 0, -1, y_up, y_down, x_left, x_left + (x_left + x_right)/20, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_up, 1, 0, y_up, y_up + (y_up + y_down)/20, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_down, 0, 1, y_up, y_down, x_right - (x_left + x_right)/20, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_down, -1, 0, y_down - (y_up + y_down)/20, y_down, x_left, x_right, cell_ptr);
		}
	} else {
		if (pos_y == y_down) {
			cell_ptr = rand_rotate(x_left, y_down, -1, 0, y_down - (y_up + y_down)/20, y_down, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_up, 0, -1, y_up, y_down, x_left, x_left + (x_left + x_right)/20, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_up, 1, 0, y_up, y_up + (y_up + y_down)/20, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_down, 0, 1, y_up, y_down, x_right - (x_left + x_right)/20, x_right, cell_ptr);
		} else {
			cell_ptr = rand_rotate(x_right, y_down, 0, 1, y_up, y_down, x_right - (x_left + x_right)/20, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_down, -1, 0, y_down - (y_up + y_down)/20, y_down, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_up, 0, -1, y_up, y_down, x_left, x_left + (x_left + x_right)/20, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_up, 1, 0, y_up, y_up + (y_up + y_down)/20, x_left, x_right, cell_ptr);
		}
	}
	return;
}

/* Create boundary counterclockwise */
void ccw_rotate(int x_left, int x_right, int y_up, int y_down, int pos_x, int pos_y) {
	cell *cell_ptr = get_cell(pos_x, pos_y);
	set_danger(cell_ptr);

	if (pos_x == x_left) {
		if (pos_y == y_up) {
			cell_ptr = rand_rotate(x_left, y_down, 0, 1, y_up, y_down, x_left, x_left + (x_left + x_right)/20, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_down, 1, 0, y_down - (y_up + y_down)/20, y_down, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_up, 0, -1, y_up, y_down, x_right - (x_left + x_right)/20, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_up, -1, 0, y_up, y_up + (y_up + y_down)/20, x_left, x_right, cell_ptr);
		} else {
			cell_ptr = rand_rotate(x_right, y_down, 1, 0, y_down - (y_up + y_down)/20, y_down, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_up, 0, -1, y_up, y_down, x_right - (x_left + x_right)/20, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_up, -1, 0, y_up, y_up + (y_up + y_down)/20, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_down, 0, 1, y_up, y_down, x_left, x_left + (x_left + x_right)/20, cell_ptr);
		}
	} else {
		if (pos_y == y_down) {
			cell_ptr = rand_rotate(x_right, y_up, 0, -1, y_up, y_down, x_right - (x_left + x_right)/20, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_up, -1, 0, y_up, y_up + (y_up + y_down)/20, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_down, 0, 1, y_up, y_down, x_left, x_left + (x_left + x_right)/20, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_down, 1, 0, y_down - (y_up + y_down)/20, y_down, x_left, x_right, cell_ptr);
		} else {
			cell_ptr = rand_rotate(x_left, y_up, -1, 0, y_up, y_up + (y_up + y_down)/20, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_left, y_down, 0, 1, y_up, y_down, x_left, x_left + (x_left + x_right)/20, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_down, 1, 0, y_down - (y_up + y_down)/20, y_down, x_left, x_right, cell_ptr);
			cell_ptr = rand_rotate(x_right, y_up, 0, -1, y_up, y_down, x_right - (x_left + x_right)/20, x_right, cell_ptr);
		}
	}
	return;
}

/* Set 350 * 350 danger square */
void set_ext_dangers() {
	int x_left, x_right, y_up, y_down;
	int rand_val;
	int pos_x, pos_y;

	/* Get corner/boundary point */
	x_left = (MAZE_DIM - INNER_DIM) / 2;
	y_up = x_left;
	x_right = x_left + INNER_DIM;
	y_down = y_up + INNER_DIM;
	
	rand_val = rand() % 4;
	if (rand_val == 0) {
		pos_x = x_left;
		pos_y = y_up;
	} else if (rand_val == 1) {
		pos_x = x_left;
		pos_y = y_down;
	} else if (rand_val == 2) {
		pos_x = x_right;
		pos_y = y_up;
	} else {
		pos_x = x_right;
		pos_y = y_down;
	} 

	/* Approximate a closed polygon within the square */
	rand_val = rand() % 2;

	if (rand_val) {
		ccw_rotate(x_left, x_right, y_up, y_down, pos_x, pos_y);
	} else {
		cw_rotate(x_left, x_right, y_up, y_down, pos_x, pos_y);
	}
}

/* Set walls in danger square */
void set_int_dangers() {
	int danger_count;
	int x, y, x_left, y_up, i;
	cell *cell_ptr;

	/* Get number of dangers */
	danger_count = rand() % (INNER_DIM * INNER_DIM / 100);
	x_left = (MAZE_DIM - INNER_DIM) / 2;
	y_up = x_left;

	for (i = 0; i < danger_count; i++) {
		/* Randomly draw spot */
		x = x_left + (rand() % INNER_DIM);
		y = y_up + (rand() % INNER_DIM);

		/* Set random danger */
		cell_ptr = get_cell(x, y);
		set_danger(cell_ptr);
	}
}

/* Set flag cell */
void set_flag(char flag[FLAG_SIZE]) {
	int x, y, mid, diff;
	cell *flag_ptr;

	/* Draw (x, y) */
	diff = MAZE_DIM - INNER_DIM;
	mid = diff / 2;
	x = rand() % diff;
	y = rand() % diff;

	while(x == mid) {
		x = rand() % diff;
	}

	while(y == mid) {
		y = rand() % diff;
	}

	/* Adjust (x, y) */
	if (x > mid) {
		x += INNER_DIM;
	}

	if (y > mid) {
		y += INNER_DIM;
	}

	/* Set flag condition */
#ifdef DEBUG
	printf("flag at: (%i, %i)\n", x, y);
#endif
	flag_ptr = get_cell(x, y);
	flag_ptr->condition = FLAG;

	/* Write flag */
	memcpy(flag_ptr->contents, flag, FLAG_SIZE);
}

/* Set starting cell */
void set_start() {
	int x, y;

	/* Set current location */
	x = (MAZE_DIM - SPAWN_DIM) / 2 + (rand() % SPAWN_DIM);
	y = (MAZE_DIM - SPAWN_DIM) / 2 + (rand() % SPAWN_DIM);

	g_location = get_cell(x, y);

	/* Make location and adjacent cells safe */
	g_location->condition = SAFE;
	g_location->right->condition = SAFE;
	g_location->left->condition = SAFE;
	g_location->up->condition = SAFE;
	g_location->down->condition = SAFE;
}

/* Function to setup maze */
void setup(char flag[FLAG_SIZE]) {
	/* Allocate maze */
	allocate_maze();

	/* Set walls */
	set_ext_dangers();
	
	/* Set extra dangers */
	set_int_dangers();

	/* Set flag */
	set_flag(flag);

	/* Set start */
	set_start();
}

/* Print maze */
void see_maze() {
	/* Print symbols left to right, top to bottom */
	cell *current_row_ptr = g_maze;
	cell *current_cell_ptr = g_maze;
	
	while(1) {
		if (current_cell_ptr == NULL) {
			if (current_row_ptr != NULL) {
				current_row_ptr = current_row_ptr->down;
				current_cell_ptr = current_row_ptr;
				printf("\n");
			}
			else {
				return;
			}
		} else {
			if (current_cell_ptr->condition == SAFE) {
				if (current_cell_ptr->x == g_location->x && current_cell_ptr->y == g_location->y) {
					printf("o");
				} else {
					printf(".");
				}
			} else if (current_cell_ptr->condition == FLAG) {
				printf("*");
			} else if (current_cell_ptr->condition == FROG) {
				printf("^");
			} else if (current_cell_ptr->condition == NEBULA) {
				printf("@");
			} else {
				printf("unknown condition");
			}
			current_cell_ptr = current_cell_ptr->right;
		}
	}
}

/* Pick random frog warning */
void warn_frog() {
	int rand_val = rand() % 3;
	if (rand_val == 0) {
		printf("ribbit\n");
	} else if (rand_val == 1) {
		printf("giggle\n");
	} else {
		printf("chirp\n");
	}
}

/* Pick random nebula warning */
void warn_nebula() {
	int rand_val = rand() % 3;
	if (rand_val == 0) {
		printf("light\n");
	} else if (rand_val == 1) {
		printf("dust\n");
	} else {
		printf("dense\n");
	}
}

/* Pick random frog loss message */
void lose_frog() {
	int rand_val = rand() % 3;
	if (rand_val == 0) {
		printf("slurp\n");
	} else if (rand_val == 1) {
		printf("ribbity!\n");
	} else {
		printf("the frog...\n");
	}
}

/* Pick random nebula loss message */
void lose_nebula() {
	int rand_val = rand() % 3;
	if (rand_val == 0) {
		printf("everything is light\n");
	} else if (rand_val == 1) {
		printf("it is crushing\n");
	} else {
		printf("intense heat\n");
	}
}

/* Check current cell and accessible cells */
int check() {
	int state = g_location->condition;

	/* If danger, exit */ 
	if (state == FROG) {
		lose_frog();
		return 0;
	} else if (state == NEBULA) {
		lose_nebula();
		return 0;
	} else if (state == FLAG) {
		g_print_array[g_location->print_flag](g_location);
		return 0;
	}
	
	/* If danger nearby, print appropriate warning */
	if (g_location->left && g_location->left->condition == FROG) {
		warn_frog();
	}

	if (g_location->left && g_location->left->condition == NEBULA) {
		warn_nebula();
	}

	if (g_location->right && g_location->right->condition == FROG) {
		warn_frog();
	}

	if (g_location->right && g_location->right->condition == NEBULA) {
		warn_nebula();
	}

	if (g_location->up && g_location->up->condition == FROG) {
		warn_frog();
	}

	if (g_location->up && g_location->up->condition == NEBULA) {
		warn_nebula();
	}

	if (g_location->down && g_location->down->condition == FROG) {
		warn_frog();
	}

	if (g_location->down && g_location->down->condition == NEBULA) {
		warn_nebula();
	}

	return 1;
}

void get_input(char* idx, int left) {
	int input;
	if(left == 0) {
		return;
	}
	input = getchar();
	if(input == '\n') {
		return;
	}
	*idx = input;
	get_input(++idx, --left);
}

/* Adjust position */
void move_loop() {
	int safe = 1;
	char input;

	/* Prompt and move while in safe state */
	while (safe) {
		/* Print position */
		printf("(%i, %i)\n", g_location->x, g_location->y);

		/* Update position */
		get_input(&input, 37);

		if (input == UP) {
			if (g_location->up != NULL) {
				g_location = g_location->up;
			}
		} else if (input == DOWN) {
			if (g_location->down != NULL) {
				g_location = g_location->down;
			}
		} else if (input == LEFT) {
			if (g_location->left != NULL) {
				g_location = g_location->left;
			}
		} else if (input == RIGHT) {
			if (g_location->right != NULL) {
				g_location = g_location->right;
			}
		}
#ifdef DEBUG
		else if (input == '!') {
			see_maze();
		}
#endif
		else {
			printf("Invalid input %s\n", &input);
		}

		/* Check position */
		safe = check();
	}
}

/* Check that indices are as expected */
void check_indices() {
	int x, y;
	cell *curr_ptr;
	cell *row_ptr = g_maze;

	y = 0;
	x = 0;

	while (y < MAZE_DIM) {
		curr_ptr = row_ptr;
		while (x < MAZE_DIM) {
			/* Check x and y indices are as expected */
			if (curr_ptr->x != x || curr_ptr->y != y) {
				printf("index problem at (%i, %i)", x, y);
			}
			/* Go to next col */
			curr_ptr = curr_ptr->right;
			x++;
		}

		/* Go to next row */
		row_ptr = row_ptr->down;
		y++;
		x = 0;
	}
}

/* Check connections are as expected */
void check_connections() {
	int x, y;
	cell *curr_ptr;
	cell *row_ptr = g_maze;

	y = 0;
	x = 0;
	
	while (y < MAZE_DIM) {
		curr_ptr = row_ptr;
		while (x < MAZE_DIM) {
			/* Check adjacent indices are as expected */
			if (x != 0 && curr_ptr->left->x != x - 1 && curr_ptr->left->y != y) {
				printf("left connection problem at (%i, %i)", x, y);
			}

			if (x != MAZE_DIM -1 && curr_ptr->right->x != x + 1 && curr_ptr->right->y != y) {
				printf("right connection problem at (%i, %i)", x, y);
			}

			if (y != 0 && curr_ptr->up->y != y - 1 && curr_ptr->up->x != x) {
				printf("up connection problem at (%i, %i)", x, y);
			}

			if (y != MAZE_DIM -1 && curr_ptr->down->y != y + 1 && curr_ptr->up->x != x) {
				printf("down connection problem at (%i, %i)", x, y);
			}

			/* Go to next col */
			curr_ptr = curr_ptr->right;
			x++;
		}

		/* Go to next row */
		row_ptr = row_ptr->down;
		y++;
		x = 0;
	}
}


/* Function to call maze setup and take user input */
int main(int argc, char* argv[]) {
	/* Get flag */
	char flag[FLAG_SIZE];

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	if (argc != 2) {
		printf("need 1 arg - flag\n");
		exit(EXIT_FAILURE);
	}
	
	memcpy(flag, argv[1], FLAG_SIZE);

	/* Set up maze */
	setup(flag);

#ifdef DEBUG
	check_indices();
	check_connections();
#endif

	/* Zero flag */
	memset(flag, 0, FLAG_SIZE);
	memset(argv[1], 0, FLAG_SIZE);

	/* Print brief guide*/
	printf("Welcome to Frog Universe in C! Can you wander to the flag?\n");
	printf("Move with w, a, s, d.\n");

	/* User input loop */
	move_loop();

	/* cleanup */
	de_allocate_maze();

	return 0;
}
