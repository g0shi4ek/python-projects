from itertools import product as pr
from inspect import signature
from PIL import Image, ImageDraw


def f(a, b, c):
    return a and b or c


def hack(f):
    def circle(f, n):

        def ras(x1, y1, x2, y2):
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        center = [[[150, 150]], [[100, 150], [200, 150]], [[100, 100], [200, 100], [150, 200]],
                  [[100, 100], [200, 100], [100, 200], [200, 200]]]

        rad = 75

        img = Image.new(mode="RGB", size=(300, 300), color="black")

        pixel = img.load()
        width, height = img.size

        for x in range(width):
            for y in range(height):
                prin = []
                for krug in center[n - 1]:
                    if ras(x, y, *krug) < rad:
                        prin.append(1)
                    else:
                        prin.append(0)
                if f(*prin):
                    pixel[x, y] = (0, 225, 0)

        draw = ImageDraw.Draw(img)
        for krug in center[n - 1]:
            draw.ellipse([krug[0] - rad, krug[1] - rad, krug[0] + rad, krug[1] + rad], outline="white")

        img.save('круги Эйлера.png')

    def eat(a, skl):

        pust = ["f" for x in range(len(a[0]))]

        for i in range(len(a)):
            for j in range(len(skl)):
                flag_eat = 1
                for k in range(len(a[0])):

                    if a[i][k] != -1 and skl[j][k] != -1:
                        if a[i][k] != skl[j][k]:
                            flag_eat = 0
                    if skl[j][k] != -1 and a[i][k] == -1:
                        flag_eat = 0
                if flag_eat == 1:
                    a[i] = pust

        a = [x[:] for x in a if x != pust]

        return a

    def glue(a):

        skl = []
        flag_skl = 0
        for i in range(len(a[0])):
            sp1 = [x for x in a if x[i] == 0]
            sp2 = [x for x in a if x[i] == 1]
            sp3 = [x[:] for x in sp1]
            sp4 = [x[:] for x in sp2]
            for j in range(len(sp3)):
                sp3[j][i] = -1
            for j in range(len(sp4)):
                sp4[j][i] = -1
            for j in sp3:
                for k in sp4:
                    if j == k and (k not in skl):
                        skl.append(k)
                        flag_skl = 1

        return a, skl, flag_skl

    def print_dnf(a):
        stroka = ''
        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j] != -1:
                    if a[i][j] == 0:
                        stroka += '~'

                    stroka += 'x' + str(j)
            stroka += ' + '
        return stroka[:-2]

    def sheffer(a):
        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j] == 0:
                    a[i][j] = "(x" + str(j) + "|" + 'x' + str(j) + ")"
                if a[i][j] == 1:
                    a[i][j] = "x" + str(j)

        for i in range(len(a)):
            for j in range(len(a[i]) - 1):
                if a[i][j] != -1 and a[i][j + 1] == -1:
                    a[i][j + 1] = a[i][j]
                elif a[i][j] != -1 and a[i][j + 1] != -1:
                    umn = "(" + str(a[i][j]) + "|" + str(a[i][j + 1]) + ")"
                    a[i][j + 1] = "(" + umn + "|" + umn + ")"
        for i in range(len(a) - 1):
            if a[i][-1] != -1 and a[i + 1][-1] == -1:
                a[i][-1] = a[i + 1][-1]
            elif a[i][-1] != -1 and a[i + 1][-1] != -1:
                sloz1 = "(" + str(a[i][-1]) + "|" + str(a[i][-1]) + ")"
                sloz2 = "(" + str(a[i + 1][-1]) + "|" + str(a[i + 1][-1]) + ")"
                a[i + 1][-1] = "(" + sloz1 + "|" + sloz2 + ")"

        print(a[-1][-1])

    def sover(f, n):
        res = []
        perem = ["x" + str(y) for y in range(n)]
        print(" ".join(perem))
        for i in pr([0, 1], repeat=n):
            print(*i, sep="  ", end="  ")

            print(bool(f(*i)))
            if f(*i):
                res.append(list(i))

        print("Совершенная ДНФ")
        print(print_dnf(res))
        return res

    n = len(str(signature(f)).split(","))

    a = sover(f, n)

    while True:

        a, skl, flag_skl = glue(a)

        a = eat(a, skl)

        a.extend(skl)
        skl = []

        if flag_skl == 0:
            break

    print("Сокращенная ДНФ")
    sokr = print_dnf(a)
    print(sokr)

    print("Базис по Шефферу")
    sheffer(a)
    if n <= 4:
        circle(f, n)


hack(f)