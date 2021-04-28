import os
import json

data = open("C:/users/elie/pythonprojects/workspace.code-workspace", "r").read()
data = json.loads(data)
for i in os.listdir("C:/users/elie/pythonprojects"):
    if ({"path": i} not in data["folders"]) and (
        os.path.isdir("home/elie/pythonprojects/" + i)
    ):
        data["folders"].append({"path": i})
for i in data["folders"]:
    if i["path"] not in os.listdir("C:/users/elie/pythonprojects/"):
        del data["folders"][data["folders"].index(i)]
data = json.dumps(data)
open("C:/users/elie/pythonprojects/workspace.code-workspace", "w").write(data)
