import os
import sys
import time
from main import *

os.chdir("/home/elie/Documents/Scolaire")
run = ManageFileType()
val = 0
for matiere in run.matiere:
    if not os.path.exists(
        "/home/elie/Documents/Scolaire/Tables/{}".format(
            "{} = {}".format(matiere, run.matiere[matiere])
        )
    ):
        os.mkdir(
            "/home/elie/Documents/Scolaire/Tables/{}".format(
                "{} = {}".format(matiere, run.matiere[matiere])
            )
        )
while True:
    os.system("git add .; git commit -m 'Save' --quiet; git push --quiet")
    run.check()
    run.check(r"/home/elie/Documents/usb")
    # os.system("black /home/elie/pythonprojects")
    if not val % 600:
        os.system("""notify-send "Vos fichiers ont bien \u00e9t\u00e9 rang\u00e9s" """)
    val += 1
    time.sleep(5)
