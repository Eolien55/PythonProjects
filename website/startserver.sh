sudo pkill nginx
sudo pkill gunicorn
sudo nginx -c C:/users/elie/pythonprojects/website/conf/nginx.conf
cd C:/users/elie/pythonprojects
gunicorn -b 127.0.0.1:5000 website:app