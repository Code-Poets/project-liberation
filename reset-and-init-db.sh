#!/bin/bash -e

psql -U postgres --command="drop database project_liberation;"
psql -U postgres --command="create database project_liberation;"
./manage.py makemigrations
./manage.py migrate
./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@codepoets.it', 'superuser')"
./manage.py load_initial_data
