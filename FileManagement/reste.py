import shutil
import os
import hachoir.metadata
import hachoir.parser
from sys import argv
import re

months = {
    "01": "Janvier",
    "02": "F\u00e9vrier",
    "03": "Mars",
    "04": "Avril",
    "05": "Mai",
    "06": "Juin",
    "07": "Juillet",
    "08": "Ao\u00fbt",
    "09": "Septembre",
    "10": "Octobre",
    "11": "Novembre",
    "12": "D\u00e9cembre",
}
if len(argv) > 1:
    pathOr = argv[1]
else:
    pathOr = "."

for folder, _, files in os.walk(pathOr):
    folder = os.path.abspath(folder)
    print(folder)
    for file in files:
        if file == "reste.exe":
            continue
        try:
            format = re.findall(r"\.[A-Za-z0-9_]+$", file)[0]
        except:
            continue
        file = folder + "/" + file
        if format not in [".AAE", ".aae"]:
            try:
                parser = hachoir.parser.createParser(file)
                with parser:
                    metadata = hachoir.metadata.extractMetadata(parser)
                    metadata
                    metadata = metadata.exportDictionary(human=False)
                DateTime = metadata["Metadata"]["creation_date"]
                year = DateTime[:4]
                month = months[DateTime[5:7]]
                city, country = None, None
            except Exception as e:
                print(e)
                continue
            path = f"./{year}/{month}/"
            if not os.path.exists(path):
                os.makedirs(path)
            name = str(len(os.listdir(path)) + 1) + format
            shutil.move(file, path + name)
