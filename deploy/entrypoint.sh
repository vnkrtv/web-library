cd /code
django-admin startproject library
mkdir /code/library/main
django-admin startapp main /code/library/main

cp /library/library/settings.py /code/library/library/settings.py
cp /migrations/author.py /code/library/main/models.py
python /code/library/manage.py makemigrations main
python /code/library/manage.py migrate main

cp /migrations/composition.py /code/library/main/models.py
python /code/library/manage.py makemigrations main
python /code/library/manage.py migrate main

cp -r /library /code
python /code/library/manage.py makemigrations
python /code/library/manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python /code/library/manage.py shell
python /code/library/manage.py runserver 0.0.0.0:8080