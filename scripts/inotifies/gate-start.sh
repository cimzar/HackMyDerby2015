#!/bin/bash

for i in {1..4};
  do
    /derby/HackMyDerby/scripts/inotifies/inotify-gate${i}.sh &
  done
