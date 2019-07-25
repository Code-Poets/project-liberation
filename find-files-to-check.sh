#!/bin/bash -e

find . -type f                                                      \
    -not -path "./project_liberation/project_liberation/settings/*" \
    -not -path "*/migrations/*"                                     \
    -name "*.py"                                                    \
