import itertools
import os
import string as s


s.printable = s.ascii_letters + s.digits


def slicingfiles(nb):
    a = open("save.txt", "r").read()
    for i in range(nb):
        open(f"{i}.txt", "w").write(
            a[
                a[i * int(len(a) / nb) :].index("\n")
                + len(a[: i * int(len(a) / nb)]) : a[
                    int((i + 1)) * int(len(a) / nb) :
                ].index("\n")
                + len(a[: int((i + 1)) * int(len(a) / nb)])
            ]
        )
    b = open(f"{nb - 1}.txt", "r").read()
    open(f"{nb}.txt", "w").write(a[a.index(b) + len(b) : len(a)])


def auth(nb):
    c = 1
    output = []
    open("save.txt", "w").write("")
    for i in range(1, nb + 1):
        generator = itertools.combinations_with_replacement(s.printable, i)
        for l in generator:
            output.append("".join(l))
            if c % 500 == 0:
                open("save.txt", "a").write("".join([i + "\n" for i in output]))
                output = []
            c += 1
    open("save.txt", "a").write("".join([i + "\n" for i in output]))


print("ok")
auth(2)
slicingfiles(500)
