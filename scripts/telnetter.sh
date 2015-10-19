#!/bin/bash

tn=`ps awx | grep telnetter.py | grep -v grep`

if [ $? -ne 0 ]
  then
#  echo "Not running"
  /derby/HackMyDerby/scripts/telnetter.py &
fi

