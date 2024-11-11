import time
import json
from collections import Counter
from math import log2
from math import ceil
from tkinter import *
from tkinter.filedialog import askopenfilename


def fix_float(f):
    c = '0.'
    for i in range(30):
        f *= 2
        c += str(int(f // 1))
        f %= 1
    return c


def codig(name, obr):
    log = []
    write = open(obr + "text.prar", "wb")
    words = open(name, "r", encoding='utf-8').read()
    print(words.name)
    m = len(words)
    freq = Counter(list(words))
    p = dict()
    p = {}
    for i in freq.keys():
        p[i] = freq[i] / m

    sorted_p = sorted(p, key=p.get, reverse=True)
    slov = {}

    for i in sorted_p:
        slov[i] = p[i]
    p = dict(slov)

    for i in p:
        log.append(ceil(abs(log2(p[i]))))

    keys = list(p.keys())
    for i in range(0, len(p) - 1):
        p[keys[i + 1]] += p[keys[i]]

    for i in range(len(p) - 1, 0, -1):
        p[keys[i]] = p[keys[i - 1]]

    p[keys[0]] = 0

    j = 0
    for i in p:
        p[i] = str(fix_float(p[i])[2:log[j] + 2])
        j += 1

    for i in p:
        s = (i.encode('utf-8') + p[i].encode('utf-8'))

    str_dict = json.dumps(p).replace(": \"", ':"').replace(', "', ',"')
    write.write(str_dict.encode('utf-8') + chr(1).encode('utf-8'))

    zacod = str()
    for i in words:
        zacod += p[i]

    for i in range(0, len(zacod), 8):
        write.write(int(zacod[i:i + 8].ljust(8, "0"), 2).to_bytes(1, 'little'))
    write.close()


def decode(name, obr):
    read = open(name, "rb").read()
    write = open(obr + "text.txt", "w", encoding='utf-8')
    data = read.split(chr(1).encode('utf-8'))
    p = json.loads(data[0].decode('utf-8'))
    p = repl(p)
    byte_data = bytes([1]).join(data[1:])
    r_by = str()
    for i in byte_data:
        z = bin(i)
        z = z[2::]
        r_by += z.zfill(8)
    buk = str()

    for i in r_by:
        buk += i
        if buk in p:
            write.write(p[buk])
            buk = ""


def dec(self):
    try:
        a = askopenfilename()
        t = time.time()
        b = a.split("/")[0:-1]
        decode(a, b)
        print(time.time() - t)
        print("Секунд выполнялось данное действие")
    except:
        pass

def cod(self):
    try:
        a = askopenfilename()
        b = a.split("/")[0:-1]
        t = time.time()
        codig(a, b)
        print(time.time() - t)
        print("Секунд выполнялось данное действие")

    except:
        pass

def repl(p):
    keys = {}
    for i in p:
        keys[p[i]] = i
    return keys


root = Tk()
root.resizable(width=False, height=False)

btn1 = Button(text = "decode", width=15)
btn2 = Button(text = "encode", width=15)
btn1.pack()
btn2.pack()
btn1.bind('<Button-1>', dec)
btn2.bind('<Button-1>', cod)

root.mainloop()