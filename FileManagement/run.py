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

show = True
if not os.path.exists("/tmp/running_files_number"):
    open("/tmp/running_files_number", "w").write("0")
with open("/tmp/running_files_number", "r") as file:
    number = file.read()
while True:
    os.system(
        "git add . >/dev/null 2>&1\ngit commit -m 'Save' >/dev/null 2>&1\ngit push >/dev/null 2>&1"
    )
    run.check()
    run.check(r"/home/elie/Documents/usb")
    if show:
        os.system("""notify-send "Vos fichiers ont bien \u00e9t\u00e9 rang\u00e9s" """)
    show = False
    time.sleep(5)
    with open("/tmp/running_files_number", "r") as file:
        if number != file.read():
            exit()
