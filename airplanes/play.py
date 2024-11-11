"""Деньги хранятся в тысячах"""
from random import random, shuffle

RawPrice = 300
DestroyerPrice = 500
WorkshopPrice = 1000
chances = [[],
           [1 / 3, 2 / 3, 5 / 6, 11 / 12],
           [1 / 4, 7 / 12, 10 / 12, 11 / 12],
           [1 / 12, 1 / 3, 2 / 3, 11 / 12],
           [1 / 12, 1 / 6, 5 / 12, 9 / 12],
           [1 / 12, 1 / 6, 1 / 3, 2 / 3]
           ]
number = 2


class Bank:
    level = 3
    RawCount = 2 * number
    MinRawPrice = 500
    RequestOnDestroyers = 2 * number
    MaxDestroyerPrice = 5500

    offer = []

    def NextLevel(self, nextlevel=-1):
        if (nextlevel != -1):
            self.level = nextlevel
        else:
            chance = random()
            if chance < chances[self.level][0]:
                self.level = 1
                self.RawCount = 1 * number
                self.MinRawPrice = 800
                self.RequestOnDestroyers = 3 * number
                self.MaxDestroyerPrice = 6500
            elif chance < chances[self.level][1]:
                self.level = 2
                self.RawCount = 1.5 * number
                self.MinRawPrice = 650
                self.RequestOnDestroyers = 2.5 * number
                self.MaxDestroyerPrice = 6000
            elif chance < chances[self.level][2]:
                self.level = 3
                self.RawCount = 2 * number
                self.MinRawPrice = 500
                self.RequestOnDestroyers = 2 * number
                self.MaxDestroyerPrice = 5500
            elif chance < chances[self.level][3]:
                self.level = 4
                self.RawCount = 2.5 * number
                self.MinRawPrice = 400
                self.RequestOnDestroyers = 1.5 * number
                self.MaxDestroyerPrice = 5000
            else:
                self.level = 5
                self.RawCount = 3 * number
                self.MinRawPrice = 300
                self.RequestOnDestroyers = 1 * number
                self.MaxDestroyerPrice = 4500
        print(f"New level of Bank: {self.level}")
        print(f"RawCount = {self.RawCount}")
        print(f"MinRawPrice = {self.MinRawPrice}")
        print(f"RequestOnDestroyers = {self.RequestOnDestroyers}")
        print(f"MaxDestroyerPrice = {self.MaxDestroyerPrice}")
        self.offer.clear()

    def RawRequest(self, i):
        amount = int(input("how many raw do you want: "))
        cost = int(input("how much money per raw: "))
        if (cost < self.MinRawPrice or amount <= 0):
            return
        self.offer.append((cost, amount, i))

    def SellTime(self, players):
        shuffle(self.offer)
        self.offer.sort(reverse=True)
        for f in self.offer:
            a = min(self.RawCount, f[1])
            players[f[2]].raw += a
            players[f[2]].money -= a * f[0]
            self.RawCount -= a
            print(f"Player {players[f[2]].name} got {a} raw and pay {a * f[0]} rub")
            if self.RawCount == 0:
                self.offer.clear()
                return
        self.offer.clear()

    def DestroyersOffer(self, i):
        amount = int(input("how many Destroyers do you offer: "))
        cost = int(input("how much money per one: "))
        if (cost > self.MaxDestroyerPrice or amount <= 0):
            return
        self.offer.append((cost, amount, i))

    def Auction(self, players):
        shuffle(self.offer)
        self.offer.sort()
        for f in self.offer:
            a = min(self.RequestOnDestroyers, f[1])
            players[f[2]].destroyers -= a
            players[f[2]].money += a * f[0]
            self.RequestOnDestroyers -= a
            print(f"Player {players[f[2]].name} sell {a} destroyers and got {a * f[0]} rub")
            if self.RequestOnDestroyers == 0:
                self.offer.clear()
                return
        self.offer.clear()


class Player:
    workshop = 2  # цеха
    futureWorkshop = []
    raw = 4  # сырьё
    destroyers = 2
    futureDestroyers = 0
    money = 10000
    name: str
    MyIP: str
    Done: bool  # конец хода
    DoneBuy: bool  # конец покупки сырья
    DoneSell: bool  # конец продажи самолётов
    DoneReq: bool  # заявка на самолёты
    DoneWorkshop: bool  # заявка на цеха

    def __init__(self):
        self.Done = False
        self.DoneSell = False
        self.DoneBuy = False
        self.DoneReq = False
        self.DoneWorkshop = False

    def setName(self, name: str):
        self.name = name

    def setIP(self, IP: str):
        self.MyIP = IP

    def Pay(self):
        MoneyWas = self.money
        print(f"Pay:\n{self.raw * RawPrice} for Raw")
        self.money -= self.raw * RawPrice
        print(f"{self.destroyers * DestroyerPrice} for Destroyer")
        self.money -= self.destroyers * DestroyerPrice
        print(f"{self.workshop * WorkshopPrice} for Workshop")
        self.money -= self.workshop * WorkshopPrice
        print(f"{MoneyWas - self.money} in total")
        print(f"Money left {self.money} rub")

    def MakeYourFuture(self):
        self.destroyers += self.futureDestroyers
        self.futureDestroyers = int(input("input number of destroyers to build: "))
        self.money -= self.futureDestroyers * 2000
        self.raw -= self.futureDestroyers

        for i in range(len(self.futureWorkshop) - 1, -1, -1):
            if self.futureWorkshop[i] == 0:
                self.workshop += 1
                self.money -= 2500
                self.futureWorkshop.pop(i)
            else:
                self.futureWorkshop[i] -= 1

        if (self.workshop < 6):
            temp = 6
            while (self.workshop + temp > 6):
                temp = int(input("input number of workshop to build: "))
                if (self.workshop + temp > 6):
                    print("maximum amount of workshops is 6")

            for _ in range(temp):
                self.money -= 2500
                self.futureWorkshop.append(4)


def NextMonth(players: list[Player]):
    global number
    for i in range(len(players)):
        print(f"Player {players[i].name} has\n{players[i].money} rub; {players[i].raw} raw:")
        bank.RawRequest(i)
    bank.SellTime(players)

    for i in range(len(players)):
        print(f"Player {players[i].name} has {players[i].destroyers} destroyers")
        bank.DestroyersOffer(i)
    bank.Auction(players)

    for i in range(len(players)):
        print(f"Player {players[i].name} has\n{players[i].money} rub; {players[i].workshop} workshops; {players[i].raw} raw:")
        players[i].MakeYourFuture()

    for i in range(len(players)):
        players[i].Pay()
    for i in range(len(players) - 1, -1, -1):
        if players[i].money <= 0:
            print(f"Player {players[i].name} is bankrot")
            players.pop(i)
            number -= 1

    bank.NextLevel()


if __name__ == "__main__":
    number = int(input("input amount the players: "))
    players = [Player() for _ in range(number)]
    bank = Bank()
    bank.NextLevel(3)

    done = False
    while not done:
        NextMonth(players)