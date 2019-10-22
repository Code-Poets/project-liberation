#!/bin/bash -e

cd company_website/
pytest 					\
	--cov-report term-missing 	\
	--cov-config ../coverage-config \
	--cov=.
rm .coverage
cd ..
