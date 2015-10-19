#!/bin/bash
WLAN=`ifconfig wlan0 | grep 'inet addr' | grep '10\.42'`

if [ $? -ne 0 ];
  then
    for i in {1..4};do
      ifdown wlan0:$i
    done
    ifdown wlan0
    ifup wlan0
    for i in {1..4};do
      ifup wlan0:$i
    done
    sleep 30
    service isc-dhcp-server restart
    service hostapd restart
fi

