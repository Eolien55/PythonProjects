'''import os

cont = """import click
@click.group()
def main():
    pass
%s
main()"""
modules = []
for i in os.listdir("C:/users/elie/pythonprojects/commands"):
    modules.append(
        'from %s import *\nfor i in commands:exec("main.add_command('
        % (i[: i.index(".")])
        + '%s)"%(i))'
    ) if not os.path.isdir(i) and not i == "commands.py" else 1 + 1
open("C:/users/elie/pythonprojects/commands/commands.py", "w").write(
    cont % "\n".join(modules)
)'''
