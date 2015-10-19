#!/bin/bash

GATE="1"
CODEFILE="/derby/gate${GATE}/code"
LOGFILE="/var/log/derby/gate${GATE}code.log"

while true
  do 
    /derby/codes-db.py -g $GATE > $CODEFILE
    inotifywait -e access $CODEFILE >> $LOGFILE 
done &

