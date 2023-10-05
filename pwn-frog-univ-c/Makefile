CFLAGS = -ansi -pedantic -Wimplicit-function-declaration -Wreturn-type -c

all: maze

maze: maze.o
	gcc maze.o -s -o maze

maze.o: maze.c
	gcc $(CFLAGS) maze.c

debug: maze_debug

maze_debug: maze_debug.o
	gcc maze_debug.o -o maze_debug

maze_debug.o: maze.c
	gcc $(CFLAGS) -D DEBUG -o maze_debug.o maze.c

clean:
	rm -rf *.o maze maze.txt maze_debug*

