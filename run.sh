sudo apt install xterm
if ! pyenv
then
	curl https://pyenv.run | bash
	xterm -e "./config"
	exit
fi
pyenv install 3.9.4
pyenv global 3.9.4
pip install ipython jupyter black gunicorn -r requirements.txt
