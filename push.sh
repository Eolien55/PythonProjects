git init
git add .
echo "Commit message : "
read commit
git commit -a -m "$commit"
git push --set-upstream git@github.com:Eolien55/PythonProjects.git master
