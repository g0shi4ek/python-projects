import os

Figures = {
    0: "nothing",
    1: "king",
    2: "queen",
    3: "rook",
    4: "bishop",
    5: "knight",
    6: "pawn"
}
Players = {
    0: "nobody",
    1: "White",
    2: "Black"
}
place = [
    [(3, 2), (5, 2), (4, 2), (2, 2), (1, 2), (4, 2), (5, 2), (3, 2)],
    [(6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 2)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(6, 1), (6, 1), (6, 1), (6, 1), (6, 1), (6, 1), (6, 1), (6, 1)],
    [(3, 1), (5, 1), (4, 1), (2, 1), (1, 1), (4, 1), (5, 1), (3, 1)]
]
CurPlayer = 1


def move(x1, y1, x2, y2):
    place[7 - y2][x2], place[7 - y1][x1] = place[7 - y1][x1], (0, 0)


def pawnRules(x1, y1, x2, y2, color):
    if place[7 - y1][x1] == (6, color):
        if color == 1:
            if place[7 - y2][x2][1] == 0 and x2 - x1 == 0:
                if y1 == 6:
                    print("You can replace pawn on something")
                    place[7 - y1][x1] = (
                    int(input("2: queen; 3: rook; 4: bishop; 5: knight\n>>>")), place[7 - y1][x1][1])
                    if not (2 <= place[7 - y1][x1][0] <= 5):
                        return 0
                if y2 - y1 == 1 or (y1 == 1 and y2 - y1 == 2):
                    move(x1, y1, x2, y2)
                    return 1
            elif place[7 - y2][x2][1] == (color % 2 + 1) and abs(x2 - x1) == 1 and y2 - y1 == 1:
                if y1 == 6:
                    print("You can replace pawn on something")
                    place[7 - y1][x1] = (
                    int(input("2: queen; 3: rook; 4: bishop; 5: knight\n>>>")), place[7 - y1][x1][1])
                    if not (2 <= place[7 - y1][x1][0] <= 5):
                        return 0
                move(x1, y1, x2, y2)
                return 1

        if color == 2:
            if place[7 - y2][x2][1] == 0 and x2 - x1 == 0:
                if y1 == 1:
                    print("You can replace pawn on something")
                    place[7 - y1][x1] = (
                    int(input("2: queen; 3: rook; 4: bishop; 5: knight\n>>>")), place[7 - y1][x1][1])
                    if not (2 <= place[7 - y1][x1][0] <= 5):
                        return 0
                if y1 - y2 == 1 or (y1 == 6 and y1 - y2 == 2):
                    move(x1, y1, x2, y2)
                    return 1
            elif place[7 - y2][x2][1] == (color % 2 + 1) and abs(x2 - x1) == 1 and y1 - y2 == 1:
                if y1 == 1:
                    print("You can replace pawn on something")
                    place[7 - y1][x1] = (
                    int(input("2: queen; 3: rook; 4: bishop; 5: knight\n>>>")), place[7 - y1][x1][1])
                    if not (2 <= place[7 - y1][x1][0] <= 5):
                        return 0
                move(x1, y1, x2, y2)
                return 1
    return 0


def kingRules(x1, y1, x2, y2, color):
    if place[7 - y1][x1] == (1, color) and place[7 - y2][x2][1] != color:
        if color == 1 or color == 2:
            if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                move(x1, y1, x2, y2)
                return 1
    return 0


def queenRules(x1, y1, x2, y2, color):
    if place[7 - y1][x1] == (2, color) and place[7 - y2][x2][1] != color:
        if color == 1 or color == 2:
            if abs(x1 - x2) == abs(y1 - y2) or x1 == x2 or y1 == y2:
                flag = True
                buffer = (x1, y1, x2, y2)
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                checkList = zip(range(x1 + 1, x2), range(y1 + 1, y2)) if abs(x1 - x2) == abs(y1 - y2) else zip(
                    [x1] * abs(y1 - y2), range(y1 + 1, y2)) if x1 == x2 else zip(range(x1 + 1, x2), [y1] * abs(x1 - x2))
                for x, y in checkList:
                    if place[7 - y][x] != (0, 0):
                        flag = False
                        break
                if flag:
                    move(*buffer)
                    return 1
    return 0


def rookRules(x1, y1, x2, y2, color):
    if place[7 - y1][x1] == (3, color) and place[7 - y2][x2][1] != color:
        if color == 1 or color == 2:
            if x1 == x2 or y1 == y2:
                flag = True
                for x, y in (*zip([x1] * abs(y1 - y2), range(min(y1, y2) + 1, max(y1, y2))),
                             *zip(range(min(x1, x2) + 1, max(x1, x2)), [y1] * abs(x1 - x2))):
                    if place[7 - y][x] != (0, 0):
                        flag = False
                        break
                if flag:
                    move(x1, y1, x2, y2)
                    return 1
    return 0


def bishopRules(x1, y1, x2, y2, color):
    if place[7 - y1][x1] == (4, color) and place[7 - y2][x2][1] != color:
        if color == 1 or color == 2:
            if abs(x1 - x2) == abs(y1 - y2):
                flag = True
                for x, y in zip(range(min(x1, x2) + 1, max(x1, x2)), range(min(y1, y2) + 1, max(y1, y2))):
                    if place[7 - y][x] != (0, 0):
                        flag = False
                        break
                if flag:
                    move(x1, y1, x2, y2)
                    return 1
    return 0


def knightRules(x1, y1, x2, y2, color):
    if place[7 - y1][x1] == (5, color) and place[7 - y2][x2][1] != color:
        if color == 1 or color == 2:
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
                move(x1, y1, x2, y2)
                return 1
    return 0


Rules = {
    0: None,
    1: kingRules,
    2: queenRules,
    3: rookRules,
    4: bishopRules,
    5: knightRules,
    6: pawnRules
}


def uchr(code: str):
    return chr(int(code.lstrip("U+").zfill(8), 16))


Symbols = (
    (" "),
    (" ", uchr("U+2654"), uchr("U+2655"), uchr("U+2656"), uchr("U+2657"), uchr("U+2658"), uchr("U+2659")),
    (" ", uchr("U+265A"), uchr("U+265B"), uchr("U+265C"), uchr("U+265D"), uchr("U+265E"), uchr("U+265F"))
)


def draw():
    os.system("cls")
    for line in range(len(place) * 2 + 1):
        if line % 2 == 0:
            print("  +---+---+---+---+---+---+---+---+")
        else:
            print(f"{8 - line // 2} |", end='')
            for fig in place[line // 2]:
                print(f" {Symbols[fig[1]][fig[0]]} |", end='')
            print()
    print("    A   B   C   D   E   F   G   H")


history = []

while 1:
    draw()
    for moment in range(len(history)):
        print(history[moment], end='\t\t')
        if moment % 10 == 9:
            print()
    print()
    try:
        x1, y1 = input(("White" if CurPlayer == 1 else "Black") + " to move. Select a figure: ")
        if x1 == '0' and y1 == '0':
            break
        y1 = int(y1) - 1
        x1 = ord(x1) - ord('a')
        if 0 <= x1 <= 7 >= y1 >= 0 and place[7 - y1][x1][0] != 0:
            x2, y2 = input("choice cell: ")
            y2 = int(y2) - 1
            x2 = ord(x2) - ord('a')
            if 0 <= x2 <= 7 >= y2 >= 0:
                if Rules[place[7 - y1][x1][0]](x1, y1, x2, y2, CurPlayer):
                    CurPlayer = CurPlayer % 2 + 1
                    history.append(f"{chr(ord('a') + x1)}{y1 + 1} - {chr(ord('a') + x2)}{y2 + 1}")
                else:
                    input("something went wrong, try again")
            else:
                input("wrong data 1")
        else:
            input("wrong data 2")
    except:
        input("wrong data 3")

draw()
