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

Price = {
    0: 0,
    1: 50,
    2: 9,
    3: 5,
    4: 3,
    5: 3,
    6: 1
}


def balance():
    res = 0
    for y in range(len(place)):
        for x in range(len(place[y])):
            res += Price[place[y][x][0]] * (1 - 2 * (place[y][x][1] == 2))
    return res


def Bot(depth):
    if depth == 5:
        return balance()
    g = [[*place[y][x], 7 - y, x] for y in range(len(place)) for x in range(len(place[y])) if place[y][x] != (0, 0)]
    best_res = 100 if depth % 2 == 1 else -100
    deal = ()
    for figure in g:
        if figure[1] == 1 + depth % 2:
            for y in range(len(place)):
                for x in range(len(place[y])):
                    WasFig = place[7 - y][x]
                    if Rules[figure[0]](figure[3], figure[2], x, y, 1 + depth % 2):
                        curRes = Bot(depth + 1)
                        if (depth % 2 == 1 and best_res > curRes) or (depth % 2 == 0 and best_res < curRes):
                            best_res = curRes
                            deal = (figure[3], figure[2], x, y)
                        move(x, y, figure[3], figure[2])
                        place[7 - y][x] = WasFig
    if depth == 1 and deal:
        move(*deal)
        history.append(f"{chr(ord('a') + deal[0])}{deal[1] + 1} - {chr(ord('a') + deal[2])}{deal[3] + 1}")
    return best_res


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
    for moment in range(len(history)):
        print(history[moment], end='\t\t')
        if moment % 10 == 9:
            print()
    print()


history = []

mode = input("Choise mod: 1 - two player; 2 - with bot\n>>> ")

while 1:
    draw()
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
                    if mode == '1':
                        CurPlayer = CurPlayer % 2 + 1
                    history.append(f"{chr(ord('a') + x1)}{y1 + 1} - {chr(ord('a') + x2)}{y2 + 1}")
                    count = 0
                    for line in place:
                        for figure in line:
                            if figure[0] == 1:
                                count += 1
                    if count != 2:
                        break
                    if mode == '2':
                        draw()
                        print("wait for bot")
                        Bot(1)
                        count = 0
                        for line in place:
                            for figure in line:
                                if figure[0] == 1:
                                    count += 1
                        if count != 2:
                            break
                else:
                    input("something went wrong, try again")
            else:
                input("wrong data 1")
        else:
            input("wrong data 2")
    except:
        input("wrong data 3")

draw()
print("Game over")