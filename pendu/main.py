import os

try:
    fichier = eval(open("scratch.txt", "r").read())
except FileNotFoundError:
    open("scratch.txt", "w").write("")
    fichier = eval(open("scratch.txt", "r").read())
ask = int(input("Ajouter un mot ou jouer ? (1/2)"))
word = 0
if ask == 2:
    import random

    errors = []
    word = random.choice(fichier)
    error = 11
    cmptError = 11
    affichage = "_" * len(word)
    while cmptError != 0:
        verif = ""
        os.system("cls")
        print(
            affichage
            + """
        """
            + str(cmptError)
        )
        l = input("Entrez une lettre : ")
        if l in affichage or l in errors:
            print("Lettre déjà mise !")
        elif l in word:
            for i in range(len(word)):
                if word[i] == l:
                    verif += l
                elif affichage[i] == "_":
                    verif += "_"
                else:
                    verif += affichage[i]
            affichage = verif
        else:
            errors.append(l)
            cmptError -= 1
        if "_" not in affichage:
            print("Victoire !")
            exit()
    print("Perdu ! Le mot était : %s" % word)
elif ask == 1:
    while not word == "":
        print(fichier)
        word = input("Mettez le mot à ajouter : ")
        if word in fichier:
            print("Mettez un  autre mot !")
        else:
            fichier.append(word)
            open("scratch.txt", "w").write(str(fichier))
