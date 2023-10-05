BUILD = build
DIST = ${BUILD}/dist.zip

8ball: 8ball.c
	mkdir -p ${BUILD}
	gcc -o ${BUILD}/8ball 8ball.c

dist.zip: 8ball
	zip $@ ${BUILD}/$<
