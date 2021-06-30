from tkinter import ttk
import tkinter as tk
import ttkthemes as themes
from tkinter import messagebox as mb
import pref_table
import schulze

colors = [
    "#80BFFF",
    "#FFFF70",
    "#FF6060",
    "#80FF70",
    "#61a854",
    "#1c9147",
    "#40ffff",
    "#ffa1c0",
    "#f59873",
    "#a159ff",
    "#ff59f7",
]
alternatives = []
ballots = []
weigths = []

################################ BASE ################################

main = themes.ThemedTk(theme="arc")
main.configure(background="#F6F4F2")
main.title("PRESENTATION")
main.geometry("")

################################ PRESENTATION ################################


def next():
    main.title("ALTERNATIVES")
    labelExpl.destroy()
    buttonExpl.destroy()
    labelEnter.grid(padx=15, pady=10, column=1)
    entryEnter.grid(padx=15, pady=10, column=1)
    labelAlts.grid(padx=15, pady=10, column=1)
    buttonPageNext.grid(padx=15, pady=10, row=4, column=0)
    buttonPagePrev.grid(padx=15, pady=10, row=4, column=2)
    buttonEnter.grid(padx=15, pady=10, column=1)
    page(realstring, number, buttonPageNext, buttonPagePrev)


buttonExpl = ttk.Button(main, text="Ok", command=next)
labelExpl = ttk.Label(
    main,
    text="""Vous devez choisir des alternatives et les entrer. 
Ensuite, vous devez mettre des TYPES de scrutin 
en cochant les cases correspondant aux préférences 
de chacun. Enfin, il vous faut entrer le nombre de 
chaque type de scrutin.""",
)
labelExpl.grid(padx=15, pady=15, column=0, row=0)
buttonExpl.grid(padx=15, pady=15, column=1, row=1)

################################ ALTERNATIVES ################################


def vote():
    if not mb.askyesno("", "Vous êtes sûr d'avoir mis TOUTES les alternatives ?"):
        return
    main.title("VOTE")
    labelEnter.destroy()
    entryEnter.destroy()
    buttonEnter.destroy()
    labelVote.grid(padx=15, pady=10, column=1)
    entryVote.grid(padx=15, pady=10, column=1)
    labelBallots.grid(padx=15, pady=10, column=1)
    ballotPageNext.grid(padx=15, pady=10, row=8, column=0)
    ballotPagePrev.grid(padx=15, pady=10, row=8, column=2)
    buttonEndBallots.grid(padx=15, pady=10, column=1)
    page(realstring, number, buttonPageNext, buttonPagePrev)
    page(realstring, ballot_number, ballotPageNext, ballotPagePrev)


def add(event):
    global realstring
    alternative = resetEnter.get()
    if alternative and alternative not in alternatives:
        alternatives.append(resetEnter.get())
        realstring = (
            realstring + "\n" + str(len(alternatives)) + " : " + resetEnter.get()
        )
        resetAlts.set(page(realstring, number, buttonPageNext, buttonPagePrev))
        labelAlts.update()
    else:
        mb.showinfo("", "Alternative déjà utilisée ou alternative incorrecte")
    resetEnter.set("")


def page(string, number, button1, button2):
    if not "\n".join(string.split("\n")[(number - 1) * 10 : number * 10]):
        button1["state"] = tk.DISABLED
    else:
        button1["state"] = tk.NORMAL
    if not "\n".join(string.split("\n")[(number + 1) * 10 : (number + 2) * 10]):
        button2["state"] = tk.DISABLED
    else:
        button2["state"] = tk.NORMAL
    return "\n".join(string.split("\n")[number * 10 : (number + 1) * 10])


def prevpage():
    global number
    number += 1
    resetAlts.set(page(realstring, number, buttonPageNext, buttonPagePrev))


def nextpage():
    global number
    number -= 1
    resetAlts.set(page(realstring, number, buttonPageNext, buttonPagePrev))


labelEnter = ttk.Label(main, text="Entrez l'alternative (= le candidat) suivant(e)")
resetEnter = tk.StringVar()
resetEnter.set("")
entryEnter = ttk.Entry(main, text=resetEnter)
entryEnter.bind("<Return>", add)
buttonEnter = ttk.Button(
    main, text="Toutes les alternatives ont été entrées", command=vote
)
resetAlts = tk.StringVar()
resetAlts.set("Ajoutées jusque là :")
labelAlts = ttk.Label(main, textvariable=resetAlts, foreground="#A0A0A0")
realstring = resetAlts.get()
buttonPageNext = ttk.Button(main, text="<", command=nextpage)
buttonPagePrev = ttk.Button(main, text=">", command=prevpage)
number = 0

################################ VOTE ################################


def prevballot():
    global ballot_number
    ballot_number += 1
    ballot_string.set(
        page(real_ballot_string, ballot_number, ballotPageNext, ballotPagePrev)
    )


def nextballot():
    global ballot_number
    ballot_number -= 1
    ballot_string.set(
        page(real_ballot_string, ballot_number, ballotPageNext, ballotPagePrev)
    )


def add_ballot(event):
    global real_ballot_string
    try:
        string_ballot = resetVote.get().split(",")[0]
        number = resetVote.get().split(",")[1]
        number = int(number)
    except:
        mb.showerror("", "Mauvaise syntaxe. Réessayez.")
        return
    ballot, string_ballot = string_to_ballot(string_ballot)
    if ballot:
        if ballot in ballots:
            mb.showerror("", "Scrutin déjà entré")
            return
        else:
            real_ballot_string += "\n" + string_ballot
            ballot_string.set(
                page(real_ballot_string, ballot_number, ballotPageNext, ballotPagePrev)
            )
            ballots.append(ballot)
            weigths.append(number)
            resetVote.set("")
    else:
        mb.showerror("", "Mauvaise syntaxe. Réessayez.")


def string_to_ballot(string):
    ballot = string.split("+")
    ballot = [i.split("-") for i in ballot]
    for i in range(len(ballot)):
        ballot[i] = list(set(ballot[i]))
        for j in range(len(ballot[i])):
            try:
                entry = ballot[i][j]
                int(entry)
                assert int(entry) <= len(
                    alternatives
                ), "Well, that'll never be seen, so wassup ?"
                ballot[i][j] = int(entry)
            except:
                return None, None
    for i in range(len(ballot)):
        for j in ballot[i]:
            if j in pref_table.concat_lists(ballot[min(i + 1, len(ballot)) :], level=1):
                return None, None
    string_ballot = "+".join(["-".join(map(str, i)) for i in ballot])
    return ballot, string_ballot


def end_vote():
    global length
    length = len(alternatives)
    entryVote.destroy()
    labelVote.destroy()
    labelBallots.destroy()
    ballotPageNext.destroy()
    ballotPagePrev.destroy()
    buttonEndBallots.destroy()
    buttonPageNext.destroy()
    buttonPagePrev.destroy()
    labelAlts.destroy()
    winner = schulze.main(pref_table.main(length, ballots, weigths))

    winner = "Liste des vainqueurs : \n" + "\n".join(
        map(alternatives.__getitem__, winner),
    )

    labelWINNAR = ttk.Label(main, text=winner)
    labelWINNAR.grid(padx=15, pady=15)


resetVote = tk.StringVar()
resetVote.set("")
entryVote = ttk.Entry(main, text=resetVote)
entryVote.bind("<Return>", add_ballot)
labelVote = ttk.Label(
    main,
    text="""Rappel pour la syntaxe : 
    [alternative]-[alternative]-...+
    [alternative]+...+[alternative],nombre. 
    - pour l'égalité entre 2 
    alternatives, + pour la 
    préférence des alternatives à 
    droite sur les alternatives à 
    gauche. Nombre pour le nombre 
    de scrutins de ce type""",
)

real_ballot_string = "Jusque-là :"
ballot_string = tk.StringVar()
ballot_string.set(real_ballot_string)
labelBallots = ttk.Label(main, textvariable=ballot_string, foreground="#A0A0A0")
ballotPageNext = ttk.Button(main, text="<", command=nextballot)
ballotPagePrev = ttk.Button(main, text=">", command=prevballot)
ballot_number = 0
buttonEndBallots = ttk.Button(
    main, text="Tous les scrutins ont été entrés", command=end_vote
)

main.mainloop()
