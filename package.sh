#!/bin/bash

PACKAGES_DIR="packages"
DIR=$(pwd)

# Freeze pipenv requirements
pipenv lock -r > requirements.txt

# Install dependencies for Linux
docker run -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/sh -c "pip install -r requirements.txt -t $PACKAGES_DIR; exit"

cd $PACKAGES_DIR
zip -r9 $DIR/lambda.zip *

cd $DIR
zip -g lambda.zip lambda.py

# Cleanup
rm -r $PACKAGES_DIR
rm requirements.txt
