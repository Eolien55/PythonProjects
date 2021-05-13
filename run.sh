sudo apt update
sudo apt install -y git vim curl python-tk python3-tk tk-dev build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev software-properties-common apt-transport-https liblzma-dev default-jre libsqlite3-dev
[[ ! -d /home/elie/.pyenv ]] && curl https://pyenv.run | bash && echo 'export PATH="/home/elie/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
' >> ~/.bashrc && exit
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.5
pyenv global 3.9.5
pip install pipreqs
! [[ -d /home/elie/pythonprojects ]] && git clone https://github.com/Eolien55/PythonProjects.git pythonprojects
cd /home/elie/pythonprojects
pipreqs . --force
pip install ipython jupyter black gunicorn -r requirements.txt
echo '# some more aliases
alias pip-="pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U"
alias o="xdg-open $@"' >> ~/.bashrc
git config --global alias.tree 'log --all --decorate --oneline --graph'
git config --global user.email "elielevaillant2007@gmail.com"
git config --global user.name "Eolien55"
sudo cp vimsettings /etc/vim/vimrc
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt install -y code
sudo apt install -y nginx
sudo apt install -y snapd
sudo snap install discord
sudo apt install -y libreoffice
chmod 700 key key.pub
cp key ~/.ssh
cp key.pub ~/.ssh
ssh-add ~/.ssh/key
chmod +x files yt-dl yt-gui
sudo cp files /bin
sudo cp yt-dl /bin
sudo cp yt-gui /bin

