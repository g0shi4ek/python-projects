import asyncio
import time
import random
import signal
import matplotlib.pyplot as plt

speed = 100
trains = []
cap = 1000
zad = 18
np = 10
poezd_size = 400
stoyanka = 15 / speed
pass_int = 1 / speed
# pereg=2.4
train_num = 7
inter = (38 / train_num) * 60 / speed
zad_nac = (18 * 60) / speed
int_stat = 60 / speed
stat_plat = []
stat_train = []
stat_time = []
num_pass = 0
time_pass = 0
sum_pass_time = 0
sum_pass_n = 0

print(stoyanka, pass_int, inter, zad_nac)

start = time.time()


def print_info(s):
    print(f"{round(time.time() - start, 3)} {s}")


class Train:
    def __init__(self, n, size):
        self.n = n
        self.size = size
        self.pass_list = [[] for x in range(5)]
        self.dir = -1
        self.sum_pass = 0
        self.station = 0
        self.x = 0

    async def move(self, x, y):
        # print("Поезд едет", x, y)
        if self.dir > 0:
            pereg = stations[x].intpr * 60 / speed
            minut = stations[x].intpr * 2
            self.x += 3
        else:
            pereg = stations[x].intobr * 60 / speed
            minut = stations[x].intobr * 2
            self.x -= 3

        for i in range(minut):
            if self.dir > 0:
                self.x += 1
            else:
                self.x -= 1
            await asyncio.sleep(pereg / minut)
        self.station = y
        if self.dir > 0:
            await stations[y].queue_pr.put(self)
        else:
            await stations[y].queue_obr.put(self)


class Pass:
    def __init__(self, station, end):
        self.start_date = time.time()
        self.start = station
        self.end = end


# class PetrolStation:
class Station:
    # SPEED = 7

    def __init__(self, n, intpr, intobr):
        self.n = n
        self.intpr = intpr
        self.intobr = intobr
        self.pass_list = [0] * 5
        self.pr_put = 0
        self.obr_put = 0
        self.queue_pr = asyncio.Queue()
        self.queue_obr = asyncio.Queue()
        self.stoyanka = 15
        self.pr_pass_queue = asyncio.Queue()
        self.obr_pass_queue = asyncio.Queue()

    async def pass_come(self):
        i = 0
        while True:
            if i == 0:
                await asyncio.sleep(zad_nac)
            i += 1
            await asyncio.sleep(pass_int)
            while True:
                nazn = random.randint(0, 4)
                if nazn == self.n:
                    continue
                # self.pass_list[nazn]+=1

                if nazn > self.n:
                    await self.pr_pass_queue.put(Pass(self.n, nazn))
                else:
                    await self.obr_pass_queue.put(Pass(self.n, nazn))

                break

    async def train_come(self, poezd):

        global sum_pass_n
        global sum_pass_time
        if self.n == 0 or self.n == 4:
            poezd.dir = -1 * poezd.dir

        poezd.sum_pass -= len(poezd.pass_list[self.n])
        while True:
            if poezd.pass_list[self.n]:
                pri_pass = poezd.pass_list[self.n].pop()
                sum_pass_n += 1
                sum_pass_time += time.time() - pri_pass.start_date
                del pri_pass

            else:
                break
        if self.pr_pass_queue.qsize() != 0 or self.obr_pass_queue.qsize() != 0:

            if poezd.dir > 0:
                while True:

                    cur_pass = await self.pr_pass_queue.get()
                    poezd.pass_list[cur_pass.end].append(cur_pass)
                    poezd.sum_pass += 1
                    if poezd.sum_pass == poezd_size or self.pr_pass_queue.qsize() == 0:
                        break

            else:
                while True:

                    cur_pass = await self.obr_pass_queue.get()
                    poezd.pass_list[cur_pass.end].append(cur_pass)
                    poezd.sum_pass += 1
                    if poezd.sum_pass == poezd_size or self.obr_pass_queue.qsize() == 0:
                        break



        # print_info(f"В поезде {poezd.n} {[len(x) for x in poezd.pass_list]} на станции {self.n}")
        await asyncio.sleep(stoyanka)
        if poezd.dir > 0:
            loop.create_task(poezd.move(self.n, self.n + 1))
        else:
            loop.create_task(poezd.move(self.n, self.n - 1))

    async def enter_train_pr(self):
        while True:
            train = await self.queue_pr.get()
            # print_info(f"Поезд {train.n}: начал посадку на станции {self.n}")
            await self.train_come(train)
        # print_info(f"Поезд {train.n}: закончил посадку на станции {self.n}")

    async def enter_train_obr(self):
        while True:
            train = await self.queue_obr.get()
            # print_info(f"Поезд {train.n}: начал посадку на станции {self.n}")
            await self.train_come(train)
        # print_info(f"Поезд {train.n}: закончил посадку на станции {self.n}")


async def main():
    async def train_start():
        i = 1
        while True:
            if i <= train_num:
                new_train = Train(i, poezd_size)
                trains.append(new_train)
                await stations[0].queue_pr.put(new_train)
                await asyncio.sleep(inter)
            else:
                break
            i += 1

    async def stat():
        while True:

            sumpass_plat = 0
            for stan in stations:
                sumpass_plat += stan.obr_pass_queue.qsize()
                sumpass_plat += stan.pr_pass_queue.qsize()
            stat_plat.append(sumpass_plat / len(stations))

            sumpass_trains = 0
            for train in trains:
                sumpass_trains += train.sum_pass
            stat_train.append(sumpass_trains / len(trains))
            if sum_pass_n == 0:
                avg = 0
            else:
                avg = sum_pass_time / sum_pass_n
            stat_time.append(avg)
            # print("Поезда, платформы, время ")
            # print(stat_train,  stat_plat, stat_time)

            await asyncio.sleep(int_stat)

    async def info():
        global sum_pass_time
        global sum_pass_n
        global avg

        while True:
            for stan in stations:
                pass

                # print_info(f"На станции {stan.n} в очереди поезда = {stan.queue_pr.qsize()} {stan.queue_obr.qsize()}")
                # print_info(
                # f"На станции {stan.n} в очереди пассажира = {stan.pr_pass_queue.qsize()} {stan.obr_pass_queue.qsize()}")

                # print(len(asyncio.all_tasks(loop)))
            # print(f"Перевезено пассажиров всего {sum_pass_n}")
            if sum_pass_n != 0:
                avg = sum_pass_time / sum_pass_n
                # print(f"Времени в среднем {avg}")
            await asyncio.sleep(5)

    async def graph():
        while True:
            strok = 10
            frame = 50

            for i in range(strok):
                if i == 0:
                    print("Рок            Соб      Кри    Зар              Биб")
                elif i == 1:
                    endstr = ""
                    for i in range(len(stations)):
                        kolpas = stations[i].obr_pass_queue.qsize() + stations[i].pr_pass_queue.qsize()
                        if i == len(stations) - 1:
                            endstr = "\n"
                        print(str(kolpas).ljust(3) + " " * stations[i].intpr * 2, end=endstr)
                elif 1 < i <= len(trains):
                    print(" " * trains[i - 2].x + "[" + str(trains[i - 2].sum_pass) + "]")
                else:
                    print(" " * 50)
            await asyncio.sleep(1 / frame)

    loop.create_task(train_start())
    loop.create_task(stat())
    loop.create_task(info())
    loop.create_task(graph())

    for i in range(5):
        loop.create_task(stations[i].pass_come())

        loop.create_task(stations[i].enter_train_obr())
        loop.create_task(stations[i].enter_train_pr())


def termination_handler(*args, **kwargs):
    # print(stat_plat)
    stat_time_speed = [x * speed for x in stat_time]
    plt.plot(stat_plat, label="Среднее кол-во пасс на платформе")
    plt.plot(stat_train, label="Среднее кол-во пасс в поезде")
    plt.plot(stat_time_speed, label="Среднее время поездки в мин")
    # plt.set_xlabel("Минуты")
    plt.legend()
    plt.show()
    exit()


stations = [Station(0, 6, 0), Station(1, 3, 6), Station(2, 2, 3), Station(3, 7, 2), Station(4, 0, 7)]

signal.signal(signal.SIGINT, termination_handler)
loop = asyncio.get_event_loop()

loop.create_task(main())
loop.run_forever()

'''
import time

def graph(trains)
  strok=13
  frame=10
  for m in range(1,100):
    for i in range(strok):
      if i==0:
         print("Авт Бел  Вор ")
      elif i==1:

        print("332  33  444 555 22 333")
      elif i==3:
        print(" "*m+"[234]")
      else:  
        print(" "*(i+m))
    time.sleep(1/frame)

  for i in range(1,10):
    print("\r"+" "*20)
  for i in range(1,10):
    if m%i==5:

      print("\r"+" "*i+"xxx",end="")
      time.sleep(0.1)
    else:
       print("\r"+" "*20)
  '''



