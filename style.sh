#!/bin/bash -e

printf "[ISORT: project-liberation]\n"
./find-files-to-check.sh | xargs isort -sl -l 120
printf "\n"

printf "[BLACK: project-liberation]\n"
./find-files-to-check.sh | xargs black --line-length 120
printf "\n"
