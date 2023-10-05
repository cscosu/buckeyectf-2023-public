CC=gcc
CFLAGS=-I.

smith.o: smith.c
	$(CC) -c -o $@ $< $(CFLAGS) -DFLAG='"${FLAG}"'

smith: smith.o
	$(CC) -o $@ smith.o $(CFLAGS)

.PHONY: clean

clean:
	rm smith *.o
