#!/bin/bash

# Run poetry virtual environment
virtualenv_path="$(
    cd  ${BASH_SOURCE%/*}/
    echo "$(poetry env info -p)"
)"

if [ -z $virtualenv_path ]; then
    RED_COLOR='\033[0;31m'
    GREEN_COLOR='\033[0;32m'
    NO_COLOR='\033[0m'
    printf "${NO_COLOR}You can create virtualenv by using command: ${GREEN_COLOR}poetry install\n"
    exit 1
fi

if [ -z $VIRTUAL_ENV ]; then
    source $virtualenv_path/bin/activate
fi

poetry update
poetry check
poetry export -f requirements.txt > requirements.txt --without-hashes
poetry export -f requirements.txt > requirements-dev.txt --without-hashes --dev
