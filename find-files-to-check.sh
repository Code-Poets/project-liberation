#!/bin/bash -e

find . -type f                  			\
    -not -path "./project_liberation/settings/*" 	\
    -not -path "*/migrations/*"             		\
    -not -name "manage.py"     				\
    -name "*.py"                            		\
