#!/usr/bin/python
import os
import sys
import sqlite3 as lite
import time
import random
from oledtest import Winstar_GraphicOLED 
from subprocess import *
from time import sleep, strftime
from datetime import datetime

lcd = Winstar_GraphicOLED()
lcd.oledReset()

#Some config
twitter = '@HackTheDerby'
sleepCount = 10 #seconds to sleep between loops
pwnedDisplayTimer = 1800 #seconds to display the pwned mesage
dhcpRecentTimer = 30 #seconds to display dhcp recents
db = '/derby/display.db'

# Locations
flagFile = "/var/lib/docker-openssh/tmp/pwn"
recentDhcpFile = "/tmp/dhcprecent" # File containing the up to the minute last host to DHCPACK

# Internal Variables
lastDisplay = None 
con = None


def getDhcpRecent():
    # Gets the recently DHCPOFFERED hostname from recentDhcpFile
    if os.path.isfile(recentDhcpFile):
        with open(recentDhcpFile,"r") as f:
            data = f.read()
        recent = data.strip()
        return recent

def getPwnMessage():
    # Gets the pwn mesage from flagFile, if it exists
    if os.path.isfile(flagFile):
        with open(flagFile) as f:
            data = f.read()
        pwn = data.strip()
        os.unlink(flagFile)
        return pwn

def hostExists(host):
    # Checks to see if host is already in the strings table
    #print 'Looking up %s' % host
    try:
        con = lite.connect(db)
        cur = con.cursor()
        sql = "SELECT * FROM strings WHERE string = ? AND stringtype = 'h' limit 1"
        cur.execute(sql, [host])
        ret = cur.fetchone()

    except lite.Error, e:
        print "Error %s" % e.args[0]
        sys.exit(3)

    finally:
        if con:
            #con.commit()
            con.close()
    return(ret)

def pwnExists(pwn,timestamp):
    # Checks to see if the pwn message is already in the strings table, within the pwn display timeout
    #print 'Looking up %s' % host
    ts = timestamp - pwnedDisplayTimer
    try:
        con = lite.connect(db)
        cur = con.cursor()
        sql = "SELECT * FROM strings WHERE string = ? AND stringtype = 'p' AND seentime > ? limit 1"
        cur.execute(sql, (pwn,ts))
        ret = cur.fetchone()

    except lite.Error, e:
        print "Error %s" % e.args[0]
        sys.exit(3)

    finally:
        if con:
            #con.commit()
            con.close()
    return(ret)


def insertString(strmsg,stringType):
    # Inserts a string into the database
    try:
        con = lite.connect(db)
        cur = con.cursor()
        sql = "INSERT INTO strings (string,stringtype) VALUES(?,?)"
        cur.execute(sql, (strmsg,stringType))

    except lite.Error, e:
        print "Error %s" % e.args[0]
        sys.exit(3)

    finally:
        if con:
            con.commit()
            con.close()

def advertise():
    # Retruns a random advertisement. 
    ads = [
        twitter,
        'Come get some',
        'Hey, look over here!'
    ]
    return(random.choice(ads))

def mostRecentPwnMessage(ts):
    # Gets the most recent PWN message from the db, if there is one
    validTime = ts - pwnedDisplayTimer
    try:
        con = lite.connect(db)
        cur = con.cursor()
        sql = "SELECT string, seentime FROM strings WHERE stringtype = 'p' AND seentime > ? AND displayed = '0' ORDER BY seentime DESC LIMIT 1"
        cur.execute(sql, [validTime])
        row = cur.fetchone()
        if row:
            timeDiff = pwnedDisplayTimer - (ts - row[1])
            ret = [row[0], timeDiff]
        else:
            ret = None

    except lite.Error, e:
        print "Error %s" % e.args[0]
        sys.exit(3)

    finally:
        if con:
            con.close()
    
    return(ret)

def mostRecentDHCP(ts):
    # Gets the most recent host from the db, if there is one. 
    validTime = ts - dhcpRecentTimer
    try:
        con = lite.connect(db)
        cur = con.cursor()
        sql = "SELECT string, seentime FROM strings WHERE stringtype = 'h' AND seentime > ? AND displayed = '0' ORDER BY seentime DESC LIMIT 1"
        cur.execute(sql, [validTime])
        row = cur.fetchone()
        if row:
            timeDiff = ts - row[1]
            ret = [row[0], timeDiff]
        else:
            ret = None

    except lite.Error, e:
        print "Error %s" % e.args[0]
        sys.exit(3)

    finally:
        if con:
            con.close()

    return(ret)

def oledDisplay(message):
    # Displays to th oled, doesn't bother if the message hasnt changed.
    global lastDisplay
    #print "Message is %s and lastDisplay is %s" % (message,lastDisplay)
    if message != lastDisplay:
        #print "Upating display"
        lcd.home()
        lcd.clear()
        #lcd.autoscroll()
        #lcd.setCursor(2,1)
        lcd.message('%s' % (message))
        lastDisplay = message
    #else:
    #    print "Did not update display"
    
def main():
    # The main program loop
    lastDisplay = None
    displayingPwn = None
    displayingHost = None
    while 1:
        newPwn = None
        newDHCP = None

        timestamp = int(time.time())
        recentDHCP = getDhcpRecent() 
        pwnMessage = getPwnMessage()
        if recentDHCP and not hostExists(recentDHCP):
            insertString(recentDHCP,'h')

        if pwnMessage and not pwnExists(pwnMessage,timestamp):
            insertString(pwnMessage,'p')
        #At this point we should have DB inserts/updates completed
        #Let's see what is in the db to display

        
        mostRecentPwn = mostRecentPwnMessage(timestamp)
        if mostRecentPwn:
            displayingPwn = '1'
        else:
            displayingPwn = None

        mostRecentHost = mostRecentDHCP(timestamp)

        if displayingPwn:
            #print "OLED: %s" % (mostRecentPwn[0])
            oledDisplay(mostRecentPwn[0])
        elif mostRecentHost:
            if displayingHost and count > '0':
                count = count - 1
            elif displayingHost and count <= '0':
                displayingHost = None
            else:
            #print "OLED: %s" % (mostRecentHost[0])
                oledDisplay(mostRecentHost[0])
                displayingHost = '1'
                count = dhcpRecentTimer / sleepCount 
        else:
            #print "OLED: %s" % (advertise())
            oledDisplay(advertise())

        sleep(sleepCount)


if __name__ == '__main__':
    main()

