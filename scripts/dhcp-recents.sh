#!/bin/bash
grep "`date '+%b %e'`" /var/log/messages | \
  grep DHCPOFFER | \
  grep -v \(`hostname`\)| \
  tail -1 | \
  awk -F\( '{print $2}'| \
  awk -F\) '{print $1}'

