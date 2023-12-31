MOVE = 0
TURNLEFT = 1
TURNRIGHT = 2
INFECT = 3
SKIP = 4
HALT = 5
JUMP = 6
JUMP_IF_NOT_NEXT_IS_EMPTY = 7
JUMP_IF_NOT_NEXT_IS_NOT_EMPTY = 8
JUMP_IF_NOT_NEXT_IS_WALL = 9
JUMP_IF_NOT_NEXT_IS_NOT_WALL = 10
JUMP_IF_NOT_NEXT_IS_FRIEND = 11
JUMP_IF_NOT_NEXT_IS_NOT_FRIEND = 12
JUMP_IF_NOT_NEXT_IS_ENEMY = 13
JUMP_IF_NOT_NEXT_IS_NOT_ENEMY = 14
JUMP_IF_NOT_RANDOM = 15
JUMP_IF_NOT_TRUE = 16

RANDOM = [
    JUMP_IF_NOT_RANDOM,
    11,
    JUMP_IF_NOT_RANDOM,
    7,
    TURNRIGHT,
    JUMP,
    14,
    TURNRIGHT,
    TURNRIGHT,
    JUMP,
    14,
    JUMP_IF_NOT_RANDOM,
    14,
    TURNLEFT,
    MOVE,
    JUMP,
    0,
]
print(len(RANDOM))
print(" ".join(str(x) for x in RANDOM))

GO_AROUND_EDGE = [
    JUMP_IF_NOT_NEXT_IS_WALL,
    3,
    TURNRIGHT,
    MOVE,
    JUMP,
    0,
]
print(len(GO_AROUND_EDGE))
print(" ".join(str(x) for x in GO_AROUND_EDGE))
