sudo pkill nginx
sudo pkill gunicorn
sudo nginx -c /home/elie/pythonprojects/website/conf/nginx.conf
cd /home/elie/pythonprojects
gunicorn -b 127.0.0.1:5000 website:app