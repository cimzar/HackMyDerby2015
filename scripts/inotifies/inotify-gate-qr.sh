#!/bin/bash

GATE="3"
CODEFILE="/derby/gate${GATE}/c.png"
LOGFILE="/var/log/derby/gate${GATE}code.log"

while true
  do 
    qrencode -o $CODEFILE `/derby/codes-db.py -g $GATE`
    inotifywait -e access $CODEFILE >> $LOGFILE 
done &

