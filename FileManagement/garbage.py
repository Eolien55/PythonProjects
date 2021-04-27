import os
import shutil
import time

for folder, _, files in os.walk("."):
    folder = os.path.abspath(folder)
    for file in files:
        goodfile = folder + "/" + file
        date = time.ctime(os.path.getctime(goodfile))
        year = date[20:24]
        month = date[4:7]
        if not os.path.exists(f"./{year}/{month}"):
            os.makedirs(f"./{year}/{month}")
        if file in os.listdir(f"./{year}/{month}"):
            continue
        shutil.move(goodfile, f"./{year}/{month}")
