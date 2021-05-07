git init
echo "Commit message : "
read commit
git add .
git commit -a -m "$($commit)"
git pull git@github.com:Eolien55/PythonProjects.git
