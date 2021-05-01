sudo apt update
sudo apt install -y git vim curl python-tk python3-tk tk-dev build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev software-properties-common apt-transport-https
[[ ! -d /home/elie/.pyenv ]] && curl https://pyenv.run | bash && echo 'export PATH="/home/elie/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
' >> ~/.bashrc && exit
pyenv install 3.9.4
pyenv global 3.9.4
pip install pipreqs
! [[ -d /home/elie/pythonprojects ]] && git clone https://github.com/Eolien55/PythonProjects.git pythonprojects
cd /home/elie/pythonprojects
pipreqs . --force
pip install ipython jupyter black gunicorn -r requirements.txt
echo '# some more aliases
alias pip-="pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U"' >> ~/.bashrc
git config --global alias.tree 'log --all --decorate --oneline --graph'
sudo cp vimsettings /etc/vim/vimrc
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt install -y code
sudo apt install -y nginx
