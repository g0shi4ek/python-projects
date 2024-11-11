from math import *


def razd(a):
    isx = 0
    oper = list("+-*/()^")
    oper += "ln sin cos tg ctg exp".split()

    stack = []

    res = []
    for i in range(len(a)):
        try:
            if (a[i] == "x" and a[i + 1] != 'p') or a[i] in oper and a[i] != "-":
                if stack:
                    res.append("".join(stack))
                    stack = []
                    res.append(a[i])
                else:
                    res.append(a[i])
            elif a[i] == "-":
                if  (a[i - 1] in oper and a[i-1]!=")") or i == 0:
                    stack.append((a[i] + a[i + 1])[0:-1])
                else:
                    if stack:
                        res.append("".join(stack))
                        stack = []
                        res.append(a[i])
                    else:
                        res.append(a[i])
            else:
                stack.append(a[i])

        except:
            res.append("x")
            isx = 1

    if stack:
        res.append("".join(stack))
    for i in res:
        if i == "x":
            isx = 1
            break

    for i in res:
        if i == "x" or i in oper:
            pass
        else:
            try:
                float(i)
            except:
                print("Неверный ввод")
                return False

    return [res, isx]


def polish(a):
    oper2 = list("+-*/^")
    prior = [0, 0, 1, 1, 2]
    oper1 = "ln sin cos tg ctg exp".split()
    oper = []
    oper += oper1
    oper += oper2
    skobk = '()'

    res = []
    stack = []
    print("p",a)
    for i in a:
        if (i not in oper and i not in skobk) or i == "x":
            res.append(i)



        elif i in oper1 or i == "(":
            stack.append(i)

        elif i == ")":
            while True:
                if stack[-1] != "(":
                    res.append(stack.pop())
                else:
                    stack.pop()
                    break
                if stack == []:
                    print("Неверно расставлены скобки")
                    return False

        elif i in oper2:

            while True:
                if stack:
                    if stack[-1] in oper1 or (stack[-1] in oper2 and prior[oper2.index(i)] <= prior[oper2.index(stack[-1])]):
                        res.append(stack.pop())
                    else:
                        break
                else:
                    break
            stack.append(i)
    for i in range(len(stack)):
        res.append(stack.pop())
    return res


def calcul(a):
    oper2 = list("+-*/^")
    oper1 = "ln sin cos tg ctg exp".split()
    oper = []
    oper += oper1
    oper += oper2
    stack = []

    for i in a:
        if i not in oper:
            stack.append(i)
        elif i in oper1:
            num = stack.pop()
            if i == "ln":
                i = "log"
                if num >= 0:
                    stack.append(str(eval("1/(tan(" + num + "))")))
                else:
                    print("метод секущих тут не коробит")
            elif i == "sin":
                if num <= 1 and num >= -1:
                    print(num)
                    stack.append(str(eval("sin(" + num + "))")))
                else:
                    print("метод секущих тут не коробит")
            elif i == "cos":
                if num <= 1 and num >= -1:
                    stack.append(str(eval("cos(" + num + "))")))
                else:
                    print("метод секущих тут не коробит")
            elif i == "tg":
                i = "tan"
            num = stack.pop()
            if i == "ctg":
                stack.append(str(eval("1/(tan(" + num + "))")))

            else:

                stack.append(str(eval(i + "(" + num + ")")))
        else:
            if i == "^":
                i = "**"
            num1 = stack.pop()
            num2 = stack.pop()
            stack.append(str(eval(num2 + i + num1)))

    return stack[0]


def secant(x1, x2):
    #try:
        E = 0.00001
        n = 0
        x = 0
        x0 = 0
        c = 0
        if f(x1) * f(x2) > 0:
            while True:
                x0 = (x1 * f(x2) - x2 * f(x1)) / (f(x2) - f(x1))
                c = f(x1) * f(x0)
                x1 = x2
                x2 = x0
                n += 1
                if c == 0:
                    break
                xm = (x1 * f(x2) - x2 * f(x1)) / (f(x2) - f(x1))
                if abs(xm - x0) < E:
                    break
            return x0
        if f(x1) * f(x2) > E:
            return "нет корней"
    #except:
    #  return "Невозможно вычислить корни на этом отрезке"
def secant1(x1 ,x2):
    try:
        E = 0.00001

        if (f(x1)) == (f(x2)):
            x2 -= 1
        x = x2 - (f(x2)/f(x2)-f(x1))*(x2-x1)
        while abs(f(x)) < E:
            x = x2 - (f(x2) / f(x2) - f(x1)) * (x2 - x1)
            if abs(x1-x) < abs(x2-x):
                x1 = x
            else:
                x2 = x
        return x if x1 <= x <= x2 else None
    except:
        return "Невозможно вычислить корни на этом отрезке"
def secant3(x1, x2):
    #if f(x1) * f(x2) > 0 or f(x1) == 0:  # наличие корня
    #    return "нет корней"
    E = 0.00001
    x0 = x2
    xm = x2 - (x2 - x1) / 10000
    while (abs(xm - x0) > E):
      tmp = xm
      xm = xm - (xm - x0) * f(xm) / (f(xm) - f(x0))
      if not x1 <= xm <= x2:
        x0 = x1
        xm = x1 + (x2 - x1) / 10000
        while (abs(xm - x0) > E):
          tmp = xm
          xm = xm - ((xm - x0) * f(xm) / (f(xm) - f(x0)))
          x0 = tmp
          if not x1 <= xm <= x2:
            return xm  # секущая убежала
        return xm
      x0 = tmp
    return xm

def integral(x1, x2):
    try:
        dx = (x2 - x1) / 1000
        s = 0
        for i in range(1000):
            a1 = f(x1 + (dx * i))
            b1 = f(x1 + (dx * (i + 1)))
            c = f(((x1 + (dx * i)) + (x1 + (dx * (i + 1)))) / 2)
            # print(type(a1),type(b1),type(c),type(dx),type(i),type(s))
            s += ((dx * (i + 1)) - (dx * i)) / 6 * (a1 + 4 * c + b1)
        return s
    except:
        return "Невозможно вычислить интеграл на этом отрезке"


def f(x):
    func = []
    for i in func1:
        if i == "x":
            func.append(str(x))
        else:
            func.append(i)

    func = polish(func)
    return calcul(func)


vvod = input()

a = vvod

res = razd(a)

skob = polish(res[0])
print("k", skob)
if res and skob:
    a = res[0]
    func1 = polish(a)
    print(func1)
    isx = res[1]

    if not isx:
        a = polish(a)
        print(calcul(a))
    else:

        x1 = float(input("Введите x1 "))
        x2 = float(input("Введите x2 "))
        vyb = int(input("Введите 1, если хотите интеграл, 2 -если корни "))
        if vyb == 1:
            print(integral(x1, x2))
        elif vyb == 2:
            print(secant3(x1, x2))

#ln(sin(8*x^2-4)-x^(-2)+4)-1.8

