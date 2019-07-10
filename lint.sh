#!/bin/bash -e

printf "[FLAKE8: project-liberation]\n"
flake8                                                                                          \
    --exclude=project_liberation/project_liberation/settings/,project_liberation/manage.py,     \
    --jobs=4                                                                                    \
    --max-line-length=120                                                                       \
    --ignore=E124,E126,E128,E131,E156,E201,E221,E222,E241,E265,E271,E272,E701,F405,E501,W503    \

printf "\n"

printf "[PYLINT: project-liberation]\n"
./find-files-to-check.sh | xargs pylint --rcfile=pylintrc
printf "\n"
