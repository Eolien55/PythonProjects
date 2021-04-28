git init
echo "Commit message : "
read commit
echo "Which branch ? [branch]"
read branch
git add .
git commit -a -m "$commit"
git push --set-upstream git@github.com:Eolien55/PythonProjects.git $branch
