import os

os.system("cd c:/users/elie/pythonprojects/histoire")


class api:
    def __init__(self):
        self.fichier = eval(open("script.txt", "r+").read())

    def modif(self):
        for i in self.fichier:
            print(i, end="   ")
        self.choice = input("Quel moment ? ")
        if self.choice != "":
            self.choix = self.fichier[self.choice]
            print(self.choix)
            self.modifi = input("Que souhaitez-vous modifier ? ")
            self.choix = self.choix[self.modifi]
            print(self.choix)
            if self.modifi != "command":
                self.put = eval(input("Entrez les données : "))
            else:
                self.put = input("Entrez les données : ")
            self.fichier[self.choice][self.modifi] = self.put
            open("script.txt", "w").write(str(self.fichier))
            return 1
        else:
            return 0

    def add(self):
        for i in self.fichier:
            for il in self.fichier[i]["indices"]:
                try:
                    a = self.fichier[il]
                except:
                    print(
                        "(",
                        i,
                        self.fichier[i]["indices"],
                        self.fichier[i]["options"],
                        self.fichier[i]["question"],
                        ")",
                        end="   ",
                    )
                    print(self.fichier)
        self.indice = input("Quel indice pour tes options ? ")
        if self.indice != "":
            self.fichier[self.indice] = {
                "question": input("Phrase(s) avant la question : "),
                "options": eval(input("Rentrez les options sous forme de liste : ")),
                "command": eval(input("Commande à exécuter sous forme de liste: ")),
                "indices": eval(input("Les indices correspondant aux options : ")),
                "optionnel": eval(
                    input(
                        "Conditions, des options, dans l ordre et sous forme de liste : "
                    )
                ),
            }
            open("script.txt", "w").write(str(self.fichier))
            return 1
        else:
            return 0


a = api()
while True:
    if a.add() + a.modif() == 0:
        break
