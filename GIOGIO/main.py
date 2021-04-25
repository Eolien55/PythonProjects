import os
import playsound
import datetime

# data = open(r"Fenêtre de l'hôte de commandes.exe", "rb").read()

truue = True
date = datetime.datetime(2021, 2, 28, 14, 20)

while True:
    if datetime.datetime.now() > date and truue:
        playsound.playsound(r"giorno theme.mp3")
        truue = False
    elif not truue:
        break
    # if not os.path.exists(r"Fenêtre de l'hôte de commandes"):
    #    open(r"Fenêtre de l'hôte de commandes.exe", "wb").write(data)
