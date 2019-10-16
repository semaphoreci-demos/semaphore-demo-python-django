# pull updated version of branch from repo
cd ${USER}.pythonanywhere.co

# perform django migration task
source ~/.env
source ~/.virtualenvs/${USER}.pythonanywhere.com/bin/activate
python manage.py migrate

# restart web application
touch /var/www/${USER}_pythonanywher_com_wsgi.py
