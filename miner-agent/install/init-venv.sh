#!/bin/bash
BASE_DIR=`dirname $0`

$BASE_DIR/../resources/pyenv/versions/3.8.5/bin/python3 -m venv $BASE_DIR/../.venv

source $BASE_DIR/../.venv/bin/activate
pip install --upgrade pip
pip install -r $BASE_DIR/requirements.txt

chmod +x $BASE_DIR/../*.py