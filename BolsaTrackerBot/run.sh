#!/bin/bash

EXEC_DIR="/opt/telegram_bots/BolsaTrackerBot"
ENV=$EXEC_DIR"/environment"

source $ENV/bin/activate
cd $EXEC_DIR
nohup python bolsa_tracker.py &
