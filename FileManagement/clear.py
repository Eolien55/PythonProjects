import os
from re import findall

for folder, _, files in os.walk("."):
    for file in files:
        file = folder+"/"+file
        THEfile = file
        if not os.path.exists(file):
            continue
        with open(file, "rb") as firstfile:
            for file in files:
                file = folder + "/" + file
                if file == THEfile:
                    continue
                if not os.path.exists(file):
                    continue
                with open(file, "rb") as comparfile:
                    if firstfile.read() == comparfile.read():
                        os.remove(file)

for folder, _, files in os.walk("."):
    length = 0
    for file in files:
        file = folder + "/" + file
        format = findall(r"\.[A-Za-z0-9_]+$", file)
        if not format:
            continue
        print(format)
        format = format[0]
        os.rename(file, folder + "/" + str(length+1)+format)
        length += 1
