import click
import os

commands = ["tree"]


@click.command()
@click.argument("directory")
def tree(directory):
    """This script print a directory tree built with the inputted directory name"""
    the_tree = {directory: {}}
    for cd, subs, files in os.walk(directory):
        cd = cd.replace("\\", "/")
        par_dirs = [cd]
        cur_dir = cd
        while cur_dir != directory:
            par_dirs = f"['{os.path.dirname(cur_dir)}']{par_dirs}"
            cur_dir = os.path.dirname(cur_dir)
        for file in files:
            exec('the_tree%s.update({"%s":None})' % (par_dirs, file))
        for sub in subs:
            exec('the_tree%s.update({"%s":{}})' % (par_dirs, cd + "/" + sub))

    def build_tree(items, build):
        build[1] += 1
        for item in items:
            if isinstance(items[item], dict):
                build[0] += (
                    "\n"
                    + ("     ") * build[1]
                    + click.style(
                        "     + "
                        + ("%s" % item)[::-1][: ("     + %s" % item)[::-1].index("/")][
                            ::-1
                        ],
                        fg="blue",
                    )
                )
                build = build_tree(items[item], build)
            else:
                build[0] += (
                    "\n"
                    + ("     ") * build[1]
                    + click.style("     • %s" % item, fg="red")
                )
        build[1] -= 1
        return build

    click.echo(build_tree(the_tree, ["", -1])[0])
tree()