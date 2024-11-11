from flask import Flask, jsonify, request
app = Flask(__name__)
import requests

HostIP = "192.168.0.169"
HostPort = "5000"
HostPortIP = (lambda x: f"http://{HostIP}:{HostPort}/" + x)

data = { "name": input() }
resp = requests.post(HostPortIP("connect"), json=data)
print(resp.json())
if resp.status_code != 200:
    exit()

done = False
while not done:
    flag = int(input("0 - exit\n1 - get info\n2 - buy raw\n3 - sell planes\n4 - produce\n5 - build\n6 - finish\n> "))
    if flag == 0:
        done = True
    elif flag == 1:
        resp = requests.get(HostPortIP("info"))
        print(resp.json())
        print(flag, resp)
    elif flag == 2:
        data = { "amount": int(input("how many raw do you want: ")),
                 "cost":   int(input("how much money per raw: ")) }
        resp = requests.post(HostPortIP("buy_raw"), json=data)
        print(resp.json()["status"])
        print(flag, resp)
    elif flag == 3:
        data = { "amount": int(input("how many Destroyers do you offer: ")),
                 "cost":   int(input("how much money per one: ")) }
        resp = requests.post(HostPortIP("sell_planes"), json=data)
        print(resp.json()["status"])
        print(flag, resp)
    elif flag == 4:
        data = { "amount": int(input("input number of destroyers to build: ")) }
        resp = requests.post(HostPortIP("produce"), json=data)
        print(flag, resp)
    elif flag == 5:
        data = { "amount": int(input("input number of workshop to build: ")) }
        resp = requests.post(HostPortIP("build"), json=data)
        print(flag, resp)
    elif flag == 6:
        resp = requests.post(HostPortIP("finish"))
        print(resp.json()["status"])
        print(flag, resp)
