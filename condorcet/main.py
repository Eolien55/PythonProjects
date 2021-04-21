import os
import tkinter as tk
from tkinter import ttk


def EXIT():
    global fenetre
    fenetre.destroy()


def scrutinCondor():
    global alt, nbSCRUTINS, scrutins, FEUILLEFINALE, feuille, schulze
    scrutins, nbscrutins, alt = scrutins, nbSCRUTINS, alt
    temporary, cmpt, cmpt2 = list([]), 0, 0
    cmptxt = ""
    for l in scrutins:
        for ls in l:
            cmptxt += ls
            if ls == "_" or ls == "=":
                temporary.append(cmptxt)
                if cmptxt == "=":
                    del temporary[-1]
                    scrutins[cmpt] = temporary
                    cmpt += 1
                    temporary = []
                cmptxt = ""
    cmpta = -1
    for a in scrutins:
        cmpta += 1
        cmptb = 0
        for b in a:
            cmptb += 1
            cmptc = 0
            for c in a:
                cmptc += 1
                TestTrue, TestTrue2 = False, False
                for d in a:
                    if "_" in d and TestTrue:
                        TestTrue2 = True
                    if cmptc > cmptb:
                        TestTrue = True
                    elif b == d:
                        TestTrue = True
                        if "_" in d:
                            TestTrue2 = True
                    if "_" in d and len(a) == 2:
                        TestTrue2 = True
                    if c == d:
                        if cmptb > cmptc and TestTrue2:
                            vs = -1
                        elif cmptb < cmptc and TestTrue2:
                            vs = 1
                        else:
                            vs = 0
                        store = "%s vs %s" % (int(b[:-1]), int(c[:-1]))
                        add = "vs*int(nbscrutins[cmpta])"
                        try:
                            feuille[store] += eval(add)
                        except KeyError:
                            feuille[store] = 0
                            feuille[store] += eval(add)
    open("victoire.txt", "w").write(str(epuration()))


def epuration():
    global feuille, FEUILLEFINALE, scrutins
    cond1 = "feuille['%s vs %s']>feuille['%s vs %s']"
    for i in alt:
        FEUILLEFINALE[i] = 0
    last = list(FEUILLEFINALE.keys())[0]
    for a in alt:
        for b in alt:
            if eval(cond1 % (a, b, b, a)):
                FEUILLEFINALE[a] += 1
            else:
                pass
    for i in FEUILLEFINALE:
        if FEUILLEFINALE[i] >= FEUILLEFINALE[last]:
            last = i
    return alt[last]


def ok():
    global fenetre
    labelEXPLICATIONS.destroy()
    btEXPLICATIONS.destroy()
    label.grid(column=2, row=0, pady=5, padx=5)
    btADD.grid(column=3, row=1, pady=5, padx=5)
    entree.grid(column=2, row=1, pady=5, padx=5)
    btITSTIMETOSTOP.grid(column=1, row=1, pady=5, padx=5)


def stop():
    global fenetre, matricetotale, labelll
    condorcet()
    scrutinCondor()
    labelENTREE.destroy()
    for letter in matricetotale:
        for l in letter:
            l.destroy()
    btENTREE.destroy()
    for l in labelll:
        l.destroy()
    ttk.Label(
        fenetre, text=open("victoire.txt", "r").read(), font=("TkDefaultFont", 30)
    ).pack(pady=5, padx=5)
    ttk.Button(fenetre, text="Ok", command=EXIT).pack(side=tk.RIGHT, pady=5, padx=5)


def Entrer():
    global fenetre, nbSCRUTINS
    nbSCRUTINS.append(entreeSCRUTINS.get())
    btENTREE.grid_remove()
    entreeSCRUTINS.grid_remove()
    labelENTREE.grid_remove()
    rst.set("")
    fenetre.update()


def clickingADD():
    global c, a, fenetre, rst
    a.append("")
    a[c] = entree.get()
    c += 1
    rst.set("")
    fenetre.update()


def destroy():
    global label, btITSTIMETOSTOP, btADD, entree, fenetre, a, c, alt, TrueFalse, btSCRUTINS

    def clickingSCRUTIN():
        temporary = ""
        scrutin = {}
        name = 0
        for i in alt:
            scrutin[i + 1] = ""
        c = 1
        for letter in matricetotale:
            for l in letter:
                l = letter[l]
                name = l[1]
                place = l[2]
                l = l[0]
                if l.instate(["selected"]):
                    if True:
                        if len(scrutin[name]) == 0:
                            scrutin[name] = "_" + str(place) + "="
                        else:
                            scrutin[name] = scrutin[name] + str(place) + "="
                c += 1
        for l in scrutin:
            temporary = temporary + scrutin[l][:-1]
        temporary += "=="
        scrutin = temporary[1:]
        scrutins.append(scrutin)
        entreeSCRUTINS.grid(column=len(a) + 2, row=2, pady=5, padx=5)
        btENTREE.grid(column=len(a) + 3, row=2, pady=5, padx=5)
        labelENTREE.grid(column=len(a) + 2, row=0, pady=5, padx=5)

    TrueFalse = True
    c = 0
    label.destroy()
    btITSTIMETOSTOP.destroy()
    btADD.destroy()
    entree.destroy()
    for i in range(len(a)):
        matricetotale.append(chk)
        for il in range(len(a)):
            il = ttk.Checkbutton()
            il.grid(
                column=i + 1,
                row=len(matricetotale[i]) - ((i - 1) * len(a)) - (len(a) - 1),
                pady=5,
                padx=5,
            )
            il = [il]
            il.append(i + 1)
            il.append(len(matricetotale[i]) - ((i - 1) * len(a)) - (len(a) - 1))
            matricetotale[i][il[0]] = il
        btSCRUTIN = ttk.Button(text="Entrer ce scrutin", command=clickingSCRUTIN)
        p = tk.Label(text=i + 1, fg="blue")
        p.grid(column=i + 1, row=0, pady=5, padx=5)
        labelll[p] = 0
    btSCRUTIN.grid(column=len(a) + 2, row=len(a) + 1, pady=5, padx=5)
    labelll[btSCRUTIN] = 0
    for i in range(len(matricetotale) - 1):
        try:
            del matricetotale[-i]
        except:
            pass
    for i in range(len(a)):
        alt[i] = a[i]
    for i in range(len(alt) + 1):
        try:
            labell = ttk.Label(text=alt[i])
            labell.grid(column=0, row=i + 1, pady=5, padx=5)
            labelll[labell] = 0
        except:
            pass
    btEXIT = ttk.Button(fenetre, text="Tous les scrutins ont été mis", command=stop)
    btEXIT.grid(column=len(a) + 2, row=len(a) + 2, pady=5, padx=5)
    labelll[btEXIT] = 0


feuille, FEUILLEFINALE = {}, {}
schulze = []
labelll = {}
nbSCRUTINS = []
scrutin = {}
scrutins = []
var = """'chk_%s_%s'%(len(matricetotale[i]), i)"""
matricetotale = []
chk = {}
cmptscrutin = 0
a = []
c = 0
TrueFalse = True
alt = dict()
color = "#cce6ff"
fenetre = tk.Tk()
fenetre.title("Scrutin de Condorcet")
label = tk.Label(fenetre, text="Rentrez ici les alternatives", fg="red")
rst = tk.StringVar()
rst.set("")
entree = ttk.Entry(fenetre, width=50, text=rst)
btADD = ttk.Button(fenetre, text="Entrer", command=clickingADD)
btITSTIMETOSTOP = ttk.Button(
    fenetre, text="Arrêter de remplir les alternatives", command=destroy
)
entreeSCRUTINS = ttk.Entry(fenetre, width=50, text=rst)
btENTREE = ttk.Button(fenetre, text="Entrer", command=Entrer)
labelENTREE = tk.Label(
    fenetre, text="Entrez ici le nombre de scrutins de ce type", fg="blue"
)
labelEXPLICATIONS = ttk.Label(
    fenetre,
    text="""Vous devez choisir des alternatives et les entrer. 
Ensuite, vous devez mettre des TYPES de scrutin 
en cochant les cases correspondant aux préférences 
de chacun. Enfin, il vous faut entrer le nombre de 
chaque type de scrutin.""",
)
btEXPLICATIONS = ttk.Button(fenetre, text="""Ok""", command=ok)
labelEXPLICATIONS.pack(pady=5, padx=5)
btEXPLICATIONS.pack(side=tk.RIGHT, pady=5, padx=5)


def condorcet():
    global alt, scrutins, alt
    for i in range(len(a)):
        alt[i + 1] = a[i]
    del alt[0]
    return scrutins, nbSCRUTINS, alt


open("victoire.txt", "w").write("")
fenetre.mainloop()
