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

(
    cd ${BASH_SOURCE%/*}/

    pytest                            \
        --cov-report term-missing     \
        --cov-config coverage-config  \
        --cov=.
    rm .coverage
)

# Disable pipenv virtual environment
exit
