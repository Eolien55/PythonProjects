from time import ctime


class attribut:
    def askAttribut(self):
        self.smt = input("Donnée du jeu : ")
        if self.smt:
            self.fichier[self.smt] = eval(input("Définir comme : "))
            self.askAttribut()

    def run(self):
        try:
            self.fichier = open("sauvegarde.txt", "r+").read()
        except:
            self.fichier = {}
            self.askAttribut()
            self.fichier["state"] = "1"
            open("sauvegarde.txt", "w").write(str(self.fichier))


class game(attribut, object):
    def __init__(self):
        attribut().run()
        self.fichier = eval(open("sauvegarde.txt", "r").read())
        self.script = eval(open("script.txt", "r").read())
        self.state = False

    def ask(self, smt):
        return input(smt + " ")

    def test(self, i):
        try:
            e = self.ask(
                eval(self.script[self.state][i])
                + " ("
                + "/".join(
                    il
                    for il in self.script[self.state]["options"]
                    if bool(
                        eval(
                            self.script[self.state]["optionnel"][
                                self.script[self.state]["options"].index(il)
                            ]
                        )
                        == True
                    )
                )
                + ") "
            ).lower()
            if not e in [i.lower() for i in self.script[self.state]["options"]]:
                print(self.fichier["__main__"])
            for il in self.script[self.state]["options"]:
                if bool(
                    eval(
                        self.script[self.state]["optionnel"][
                            self.script[self.state]["options"].index(il)
                        ]
                    )
                ):
                    if e == il.lower():
                        exec(
                            self.script[self.state]["command"][
                                self.script[self.state]["options"].index(il)
                            ]
                        )
                        return self.script[self.state]["indices"][
                            [
                                i.lower() for i in self.script[self.state]["options"]
                            ].index(e)
                        ]
        except KeyError or ValueError:
            if e == "":
                if self.ask("Voulez-vous arrêter ? (o/n)").lower() == "o":
                    with open("sauvegarde.txt", "w") as f:
                        f.write(str(self.fichier))
                    exit()
            print("aie")
            return self.test(i)

    def __call__(self):
        self.state = self.fichier["state"]
        for i in self.script[self.state]:
            if i == "question":
                self.fichier["state"] = self.test(i)
        self.state = self.fichier["state"]
        return self.__call__()


Game = game()
Game()
