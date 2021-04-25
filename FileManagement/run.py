import importlib as im
import updateCommandsImports
import updateWorkspace
import types
import traceback
import os
import sys
import time
from main import *

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
    run.check()
    run.check(r"/home/elie/Documents/usb")
    im.reload(updateWorkspace)
    os.system("black /home/elie/pythonprojects")
    im.reload(updateCommandsImports)
    if not val % 600:
        os.system("""notify-send "Vos fichiers ont bien \u00e9t\u00e9 rang\u00e9s" """)
    val += 1
    time.sleep(0.5)
