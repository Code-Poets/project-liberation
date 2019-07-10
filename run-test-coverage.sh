#!/bin/bash -e

cd project_liberation/
pytest 					            \
	--cov-report term-missing 	    \
	--cov-config ../coverage-config \
	--cov=.
rm .coverage
cd ..
