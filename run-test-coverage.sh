#!/bin/bash -e

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

(
    cd ${BASH_SOURCE%/*}/

    pytest                            \
        --cov-report term-missing     \
        --cov-config coverage-config  \
        --cov=.
    rm .coverage
)

# Disable poetry virtual environment
exit
