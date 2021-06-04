import time
import os
import shutil
import traceback
import re


class ManageFileType:
    def __init__(self):
        self.matiere = {
            "Fr": "Français",
            "En": "Anglais",
            "Hg": "Histroire-Géographie",
            "Tech": "Technologie",
            "Chin": "Chinois",
            "Edmus": "Education Musicale",
            "Math": "Mathématiques",
            "Glb": "Global",
            "Gre": "Grec",
            "ArP": "Art Plastique",
            "Svt": "SVT",
            "PC": "Physique-Chimie",
        }  # TODO mettre toutes les matières
        self.mois = {
            "Jan": "Janvier",
            "Feb": "Février",
            "Mar": "Mars",
            "Apr": "Avril",
            "May": "Mai",
            "Jun": "Juin",
            "Jul": "Juillet",
            "Aug": "Août",
            "Sep": "Septembre",
            "Oct": "Octobre",
            "Nov": "Novembre",
            "Dec": "Décembre",
        }

    def check(self, path=r"/home/elie/Documents/Scolaire"):
        for folder, a, files in os.walk(path):
            for file in files:
                file = self.check_correct(file, folder)
                try:
                    command = "self.command(%s" % (
                        ".".join(file.split(".")[:-1])
                    ) + ",path=r'''{}/{}''',file='''{}''')".format(folder, file, file)
                    exec(command)
                except Exception as e:
                    # error = traceback.format_exc()
                    # print(error, file)
                    pass
            # input()

    def command(
        self,
        na: str,
        m: str = "Glb",
        file: str = None,
        path: str = None,
        fold: str = None,
    ):
        assert file and path, "Lack of errors"
        if fold is None:
            if not os.path.exists(
                r"/home/elie/Documents/Scolaire/%s/%s/%s"
                % (
                    time.ctime(os.path.getctime(path))[20:24],
                    self.matiere[m],
                    self.mois[time.ctime(os.path.getctime(path))[4:7]],
                )
            ):
                os.makedirs(
                    r"/home/elie/Documents/Scolaire/%s/%s/%s"
                    % (
                        time.ctime(os.path.getctime(path))[20:24],
                        self.matiere[m],
                        self.mois[time.ctime(os.path.getctime(path))[4:7]],
                    )
                )
        else:
            if not os.path.exists(
                r"/home/elie/Documents/Scolaire/%s/%s/%s/%s"
                % (
                    time.ctime(os.path.getctime(path))[20:24],
                    self.matiere[m],
                    fold,
                    self.mois[time.ctime(os.path.getctime(path))[4:7]],
                )
            ):
                os.makedirs(
                    r"/home/elie/Documents/Scolaire/%s/%s/%s/%s"
                    % (
                        time.ctime(os.path.getctime(path))[20:24],
                        self.matiere[m],
                        fold,
                        self.mois[time.ctime(os.path.getctime(path))[4:7]],
                    )
                )
        newpath = (
            r"/home/elie/Documents/Scolaire/%s/%s/%s/%s"
            % (
                time.ctime(os.path.getctime(path))[20:24],
                self.matiere[m],
                fold,
                self.mois[time.ctime(os.path.getctime(path))[4:7]],
            )
            if fold
            else r"/home/elie/Documents/Scolaire/%s/%s/%s"
            % (
                time.ctime(os.path.getctime(path))[20:24],
                self.matiere[m],
                self.mois[time.ctime(os.path.getctime(path))[4:7]],
            )
        )
        if m in self.matiere.keys():
            shutil.move(path, os.path.join(newpath, na + "." + file.split(".")[-1]))
            print(f'File "{na}" has been moved to "{newpath}"')

    @staticmethod
    def check_correct(file, path):
        if len(file.split(",")) != 2:
            return file
        if len(re.findall(r"('|\")", file)) >= 4:
            newfile = re.sub(r"([^^,])('|\")([^.,])", r"\1\3", file)
            if file != newfile:
                os.system(
                    f'mv "{os.path.join(path,file)}" "{os.path.join(path,newfile)}" &>/dev/null'
                )
            return newfile
        return file
