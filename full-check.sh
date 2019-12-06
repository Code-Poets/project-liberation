#!/bin/bash

# This is setup to disable warning "Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project"
export PIPENV_VERBOSITY=-1

# Run pipenv virtual enviroment
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

source $virtualenv_path/bin/activate
printf "=============== VIRTUAL ENVIRONMENT PACKAGES CHECKS ================\n"
${BASH_SOURCE%/*}/check-environment-packages.sh
printf "\n"

printf "===============DOWNLOAD AND ADD IMAGES TO DJANGO ===================\n"
${BASH_SOURCE%/*}/download-and-add-images-to-django.sh
printf "\n"

printf "=================== DJANGO CONFIGURATION CHECKS ====================\n"
python ${BASH_SOURCE%/*}/manage.py check
printf "\n"

printf "=========================== CODING STYLE ===========================\n"
${BASH_SOURCE%/*}/style.sh
printf "\n"

printf "=============================== LINT ===============================\n"
${BASH_SOURCE%/*}/lint.sh
printf "\n"

printf "========================= MYPY STATIC TYPE CHECKER =================\n"
mypy --config-file=${BASH_SOURCE%/*}/mypy.ini ${BASH_SOURCE%/*}
printf "\n"

printf "========================= REGENERATE STATIC FILES =================\n"
${BASH_SOURCE%/*}/reload-statics.sh
printf "\n"

printf "========================= UNIT TESTS WITH COVERAGE =================\n"
# NOTE: 'manage.py test' does not find all tests unless we run it from within the app directory.
${BASH_SOURCE%/*}/run-test-coverage.sh
printf "\n"

# Exit from pipenv virtual environment
exit
