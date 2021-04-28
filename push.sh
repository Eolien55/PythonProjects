git init
git add .
echo "Commit message : "
read commit
echo "\nSpecial branch ? [branch/n]"
read branch
if [ $branch != "n" ] 
then
	git checkout $branch
else 
	git checkout master
fi
git commit -a -m "$commit"
git push --set-upstream git@github.com:Eolien55/PythonProjects.git $branch
