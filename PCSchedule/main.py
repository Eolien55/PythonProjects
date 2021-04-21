class schedule:
    def __init__(self):
        self.emploi = eval(
            open(r"/home/elie/pythonprojects/PCSchedule/schedule.txt", "r").read()
        )
        self.temp = ""
        self.templist = []
        self.borne = None

    def config(self):
        fin = input("Heure de fin : ")
        action = input("Action : ")
        cb = input(
            "Vous souhaitez réaliser cette action autant de fois que possible ou une fois ? (1/beaucoup) "
        )
        if fin == "del":
            del self.emploi[int(input("\n".join(str(i) for i in self.emploi)))]
            fin, action, cb = self.config()
        return fin, action, cb

    def add(self):
        fin, action, cb = self.config()
        try:
            int(cb)
            action = "global runOrNot\nif runOrNot:" + action + "\nrunOrNot=False"
        except ValueError:
            pass
        if not action:
            return 0
        else:
            self.borne = fin
            self.emploi.append([self.borne, action])
            lenght = range(len(self.emploi))
            for _ in lenght:
                for i in self.emploi:
                    if not self.temp:
                        self.temp = i
                    if (
                        i[0] > self.temp[0]
                        or len(self.emploi) == 1
                        and i not in self.templist
                    ):
                        self.temp = i
                self.templist.append(self.emploi[self.emploi.index(self.temp)])
                del self.emploi[self.emploi.index(self.temp)]
                self.temp = ""
            self.emploi = self.templist[::-1]
            self.temp, self.templist = "", []
            open(r"/home/elie/pythonprojects/PCSchedule/schedule.txt", "w").write(
                str(self.emploi)
            )
            print(
                "\n".join(
                    [
                        str(i)
                        for i in eval(
                            open(
                                r"/home/elie/pythonprojects/PCSchedule/schedule.txt",
                                "r",
                            ).read()
                        )
                    ]
                )
            )
            return 1


pc = schedule()
while True:
    if not pc.add():
        break
print(pc.emploi)
