#!/bin/bash


ENV_DIR="../environment"

if [ ! -d "$ENV_DIR" ]; then
	virtualenv $ENV_DIR
	source $ENV_DIR/bin/activate
	## https://github.com/leandrotoledo/python-telegram-bot
	## https://pypi.python.org/pypi/python-telegram-bot/1.1
	pip install -r requirements.txt  
else
	echo "Directory '$ENV_DIR' exists, please remove it before executing the setup script"
fi
