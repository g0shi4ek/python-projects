from flask import Flask, jsonify, request
from play import Player, Bank, shuffle, number, RawPrice, DestroyerPrice, WorkshopPrice
import requests
import sys

app = Flask(__name__)

AmountOfPlayers = int(sys.argv[3])
players = [Player() for _ in range(AmountOfPlayers)]
AlreadyPlayers = 0
bank = Bank()
bank.NextLevel(3)

CurMonth = 0
month = 10 ** 10
if len(sys.argv) == 5:
    month = int(sys.argv[4])

States = [
    "waiting",
    "play",
    "finish"
]
CurState = States[0]


@app.route("/")
def route():
    return "Hello"


@app.post("/connect")
def connect():
    global AlreadyPlayers, CurState
    if CurState == States[0]:
        name = request.json.get("name", "")
        # print(f"====================== name = {name} ======================")
        players[AlreadyPlayers].setName(name)
        players[AlreadyPlayers].setIP(request.remote_addr)
        print(f"====================== addres = {request.remote_addr} ======================")
        AlreadyPlayers += 1
        if AlreadyPlayers == AmountOfPlayers:
            CurState = States[1]
            data = {"status": "game started"}
            return jsonify(data)

        else:
            data = {"status": "please wait"}
            return jsonify(data)

    # print(f"====================== name = {players[AlreadyPlayers - 1].name} ======================")
    # print("====================== data = {} ======================".format(data["status"]))
    return jsonify(status="ok")


@app.get("/info")
def info():
    """Должен возвращать текущий номер месяца, полную информацию о рынке, информацию о состоянии дел всех игроков,
    а также информацию о последних аукционах сырья и самолетов, т.е. каким игрокам и по каким ценам было продано сырье,
    у кого и по каким ценам были приобретены самолеты."""
    data = {"month": CurMonth,
            "bank.level": bank.level,
            "bank.RawCount": bank.RawCount,
            "bank.MinRawPrice": bank.MinRawPrice,
            "bank.RequestOnDestroyers": bank.RequestOnDestroyers,
            "bank.sell": bank.SellTime(players),
            "bank.auction": bank.Auction(players)


            }
    return jsonify(data)


@app.post("/buy_raw")
def buy_raw():
    amount = int(request.json.get("amount", ""))
    cost = int(request.json.get("cost", ""))
    if (cost < bank.MinRawPrice or amount <= 0):
        data = {"status": "not accepted"}
        return jsonify(data)
    else:
        for i in range(len(players)):
            if request.remote_addr == players[i].MyIP and not players[i].DoneBuy and not players[i].Done:
                bank.offer.append((cost, amount, i))
                players[i].DoneBuy = True

                flag = True
                for p in players:
                    flag = flag and p.DoneBuy

                if flag:
                    shuffle(bank.offer)
                    bank.offer.sort(reverse=True)
                    for f in bank.offer:
                        a = min(bank.RawCount, f[1])
                        players[f[2]].raw += a
                        players[f[2]].money -= a * f[0]
                        bank.RawCount -= a
                        print(f"Player {players[f[2]].name} got {a} raw and pay {a * f[0]} rub")
                        if bank.RawCount == 0:
                            break
                    bank.offer.clear()
                data = {"status": "accepted"}
                return jsonify(data)
            else:
                data = {"status": "you have already sent a request"}
                return jsonify(data)


@app.post("/sell_planes")
def sell_planes():
    amount = int(request.json.get("amount", ""))
    cost = int(request.json.get("cost", ""))
    if (cost > bank.MaxDestroyerPrice or amount <= 0):
        data = {"status": "not accepted"}
        return jsonify(data)
    else:
        for i in range(len(players)):
            if request.remote_addr == players[i].MyIP and not players[i].DoneSell and not players[i].Done:
                bank.offer.append((cost, amount, i))
                players[i].DoneSell = True
                data = {"status": "accepted"}

                flag = True
                for p in players:
                    flag = flag and p.DoneBuy

                if flag:
                    shuffle(bank.offer)
                    bank.offer.sort()
                    for f in bank.offer:
                        a = min(bank.RequestOnDestroyers, f[1])
                        players[f[2]].destroyers -= a
                        players[f[2]].money += a * f[0]
                        bank.RequestOnDestroyers -= a
                        print(f"Player {players[f[2]].name} sell {a} destroyers and got {a * f[0]} rub")
                        if bank.RequestOnDestroyers == 0:
                            break
                    bank.offer.clear()
                return jsonify(data)
            else:
                data = {"status": "you have already sent a request"}
                return jsonify(data)

    return jsonify(status="ok")


@app.post("/produce")
def produce():
    for i in range(len(players)):
        if request.remote_addr == players[i].MyIP and not players[i].Done and not players[i].DoneReq:
            players[i].destroyers += players[i].futureDestroyers
            players[i].futureDestroyers = int(request.json.get("amount", ""))
            players[i].money -= players[i].futureDestroyers * 2000
            players[i].raw -= players[i].futureDestroyers
            players[i].DoneReq = True

    return jsonify(status="ok")


@app.post("/build")
def build():
    for i in range(len(players)):
        if request.remote_addr == players[i].MyIP and not players[i].Done and not players[i].DoneWorkshop:
            players[i].DoneWorkshop = True
            for i in range(len(players[i].futureWorkshop) - 1, -1, -1):
                if players[i].futureWorkshop[i] == 0:
                    players[i].workshop += 1
                    players[i].money -= 2500
                    players[i].futureWorkshop.pop(i)
                else:
                    players[i].futureWorkshop[i] -= 1

            if (players[i].workshop < 6):
                temp = int(request.json.get("amount", ""))
                if (players[i].workshop + temp <= 6):
                    # data = {"status": "maximum amount of workshops is 6"}
                    # requests.post("http://" + request.remote_addr, json=data)

                    for _ in range(temp):
                        players[i].money -= 2500
                        players[i].futureWorkshop.append(4)

    return jsonify(status="ok")


@app.post("/finish")
def finish():
    global CurMonth, number
    for i in range(len(players)):
        if request.remote_addr == players[i].MyIP:
            players[i].Done = True
            players[i].DoneBuy = False
            players[i].DoneSell = False
            players[i].DoneReq = False
            players[i].DoneWorkshop = False

    flag = True
    for i in range(len(players)):
        flag = flag and players[i].Done

    res = "wait other players"
    if flag:
        res = ""
        for i in range(len(players)):
            MoneyWas = players[i].money
            res += f"Pay:\n{players[i].raw * RawPrice} for Raw\n"
            players[i].money -= players[i].raw * RawPrice
            res += f"{players[i].destroyers * DestroyerPrice} for Destroyer\n"
            players[i].money -= players[i].destroyers * DestroyerPrice
            res += f"{players[i].workshop * WorkshopPrice} for Workshop\n"
            players[i].money -= players[i].workshop * WorkshopPrice
            res += f"{MoneyWas - players[i].money} in total\n"
            res += f"Money left {players[i].money} rub\n"
        for i in range(len(players) - 1, -1, -1):
            if players[i].money <= 0:
                print(f"Player {players[i].name} is bankrot")
                players.pop(i)
                number -= 1
        CurMonth += 1
        bank.NextLevel()
    data = {"status": res}
    requests.post("http://" + request.remote_addr, json=data)
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host=sys.argv[1], port=int(sys.argv[2]))

# from flask import Flask
# from gevent.pywsgi import WSGIServer
# from application import app

# http_server = WSGIServer(('', 5000), app)
# http_server.serve_forever()



