import time
import os
import shutil


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

    def check(self, path=r"C:/users/elie/Documents/Scolaire"):
        for folder, a, files in os.walk(path):
            for file in files:
                try:
                    command = "self.command(%s" % (
                        file[: file.index(".")]
                    ) + ",path=r'''{}/{}''',file='''{}''')".format(folder, file, file)
                    exec(command)
                except:
                    pass

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
                r"C:/users/elie/Documents/Scolaire/%s/%s/%s"
                % (
                    time.ctime(os.path.getctime(path))[20:24],
                    self.matiere[m],
                    self.mois[time.ctime(os.path.getctime(path))[4:7]],
                )
            ):
                os.makedirs(
                    r"C:/users/elie/Documents/Scolaire/%s/%s/%s"
                    % (
                        time.ctime(os.path.getctime(path))[20:24],
                        self.matiere[m],
                        self.mois[time.ctime(os.path.getctime(path))[4:7]],
                    )
                )
            run = """shutil.move(path,r"C:/users/elie/Documents/Scolaire/%s/%s/%s/%s"%(time.ctime(os.path.getctime(path))[20:24],self.matiere[m],self.mois[time.ctime(os.path.getctime(path))[4:7]],na+file[file.index('.'):]))"""
        else:
            if not os.path.exists(
                r"C:/users/elie/Documents/Scolaire/%s/%s/%s/%s"
                % (
                    time.ctime(os.path.getctime(path))[20:24],
                    self.matiere[m],
                    self.mois[time.ctime(os.path.getctime(path))[4:7]],
                    fold,
                )
            ):
                os.makedirs(
                    r"C:/users/elie/Documents/Scolaire/%s/%s/%s/%s"
                    % (
                        time.ctime(os.path.getctime(path))[20:24],
                        self.matiere[m],
                        self.mois[time.ctime(os.path.getctime(path))[4:7]],
                        fold,
                    )
                )
            run = """shutil.move(path,r"C:/users/elie/Documents/Scolaire/%s/%s/%s/%s/%s"%(time.ctime(os.path.getctime(path))[20:24],self.matiere[m],self.mois[time.ctime(os.path.getctime(path))[4:7]],fold,na+file[file.index('.'):]))"""
        newpath = (
            r"C:/users/elie/Documents/Scolaire/%s/%s/%s/%s"
            % (
                time.ctime(os.path.getctime(path))[20:24],
                self.matiere[m],
                self.mois[time.ctime(os.path.getctime(path))[4:7]],
                fold,
            )
            if fold
            else r"C:/users/elie/Documents/Scolaire/%s/%s/%s"
            % (
                time.ctime(os.path.getctime(path))[20:24],
                self.matiere[m],
                self.mois[time.ctime(os.path.getctime(path))[4:7]],
            )
        )
        if m in self.matiere.keys():
            exec(run)
            print(f'File "{na}" has been moved to "{newpath}"')


ManageFileType().check()
