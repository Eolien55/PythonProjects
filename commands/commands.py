import click


@click.group()
def main():
    pass


from tree import *

for i in commands:
    exec("main.add_command(%s)" % (i))
main()
