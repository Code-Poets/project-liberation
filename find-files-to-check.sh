#!/bin/bash -e

find ${BASH_SOURCE%/*}                                            \
    -type f                                                       \
    -not -path "${BASH_SOURCE%/*}/project_liberation/settings/*"  \
    -not -path "*/migrations/*"                                   \
    -not -name "manage.py"                                        \
    -name "*.py"
