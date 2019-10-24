#!/bin/bash -e

# This is setup to disable warning "Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project"
export PIPENV_VERBOSITY=-1

# Run pipenv virtual environment
virtualenv_path="$(
    cd  ${BASH_SOURCE%/*}/
    echo "$(pipenv --venv)"
)"

if [ -z $virtualenv_path ]; then
    RED_COLOR='\033[0;31m'
    GREEN_COLOR='\033[0;32m'
    NO_COLOR='\033[0m'
    printf "${NO_COLOR}You can create virtualenv by using command: ${GREEN_COLOR}pipenv install --dev\n"
    exit 1

fi

if [ -z $VIRTUAL_ENV ]; then
    source $virtualenv_path/bin/activate
fi

printf "[FLAKE8: project-liberation]\n"
flake8                                                                                          \
    --exclude="${BASH_SOURCE%/*}/project_liberation/settings/"                                  \
    --jobs=4                                                                                    \
    --max-line-length=120                                                                       \
    --ignore=E124,E126,E128,E131,E156,E201,E221,E222,E241,E265,E271,E272,E701,F405,E501,W503    \
    ${BASH_SOURCE%/*}

printf "\n"

printf "[PYLINT: project-liberation]\n"
${BASH_SOURCE%/*}/find-files-to-check.sh | xargs pylint --rcfile=${BASH_SOURCE%/*}/pylintrc
printf "\n"

# Disable pipenv virtual environment
exit
