#!/bin/bash -e
./manage.py collectstatic --noinput --clear --force-color --verbosity 0
echo "OK"
