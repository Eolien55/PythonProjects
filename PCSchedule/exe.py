import asyncio
import time
import subprocess


runOrNot = True
last = "i"


class run:
    async def show_notif(self, i):
        subprocess.call(["notify-send", f"Action number {i + 1} has been performed"])
        print(f"Action number {i + 1} has been performed")

    async def check(self, i, file):
        global last, runOrNot
        if file[(i - 1)][0] < time.strftime("%X") <= file[i][0]:
            if last:
                if last != i:
                    runOrNot = True
            true = False
            if runOrNot and "runOrNot" in file[i][1]:
                true = True
            exec(file[i][1])
            if true:
                await asyncio.wait([self.show_notif(i)])
            last = i

    async def main_process(self):
        global runOrNot, last
        while True:
            time.sleep(5)
            try:
                file = open(
                    r"C:/users/elie/pythonprojects/PCSchedule/schedule.txt", "r"
                ).read()
                break
            except:
                pass
        file = eval(file)
        await asyncio.wait([self.check(i, file) for i in range(len(file))])


Run = run()
while True:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Run.main_process())
