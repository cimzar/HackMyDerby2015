#!/usr/bin/python
import os
import sys
import sqlite3 as lite
import time
import random
import re
from oledtest import Winstar_GraphicOLED 
import ledfun as oled
from subprocess import *
from time import sleep, strftime
from datetime import datetime

#sleep(30)
lcd = Winstar_GraphicOLED()
lcd.oledReset()
#sleep(10)
oled.init_display()
#sleep(10)
oled.display_off()
#sleep(10)
oled.display_on(show_cursor=False)
#sleep(10)
oled.lib_credits()

#Some config
twitter = '@HackTheDerby'
sleepCount = 10 #seconds to sleep between loops
pwnedDisplayTimer = 1800 #seconds to display the pwned message
dhcpRecentTimer = 30 #seconds to display dhcp recents
db = '/derby/display.db'

# Locations
flagFile = "/var/lib/docker-openssh/tmp/pwn"
recentDhcpFile = "/tmp/dhcprecent" # File containing the up to the minute last host to DHCPACK

# Internal Variables
lastDisplay = None 
con = None
adLoopCount = 0
ownerTwitter = None

def getDhcpRecent():
    # Gets the recently DHCPOFFERED hostname from recentDhcpFile
    if os.path.isfile(recentDhcpFile):
        with open(recentDhcpFile,"r") as f:
            data = f.read()
        recent = data.strip()
        return recent

def getPwnMessage():
    # Gets the pwn message from flagFile, if it exists
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
    global lastDisplay
    global adLoopCount
    global ownerTwitter
    currentHour = datetime.now().hour
    if currentHour >= 20 or currentHour <= 2:
        partyMode()
    else:
        ads = [
            twitter,
            'Free Hugs!',
            '___ all the ___!',
            'Hack the Planet!',
            'We like beer.',
            'Ice? Not so much',
            'Hack 4 Charities',
            'Chess?',
            'Ironliver comp.',
            '@starkdong',
            'LiverStrong!',
            'CTF fun for all!'
        ]
        if adLoopCount >= 5:
            message = 'Join my SSID:'
            ssid = getSSID() 
            adLoopCount = 0
            oled.chompit()
            oled.set_pos(0,0)
            oled.write_string('There are many')
            oled.set_pos(1,0)
            oled.write_string('derbies but')
            sleep(5)
            oled.clear_display()
            oled.set_pos(0,0)
            oled.write_string('This one is')
            oled.set_pos(1,0)
            owner = ownerTwitter + '\'s'
            oled.write_string(owner.center(16))
            sleep(10)
            oled.chompit()
            oled.set_pos(0,0)
            oled.shift_display(right=True, count=16)
            oled.write_string(message)
            oled.shift_display(right=False, count=16)
            sleep(1)
            oled.set_pos(1,0)
            oled.write_string(ssid.center(16))
            sleep(10)
            oled.chompit()
            oled.set_pos(0,0)
            oled.write_string('Information at:')
            oled.set_pos(1,0)
            oled.write_string('http://hmd.lafayette.edu')
            for shift in range(8):
                oled.shift_display(right=False, count=1)
                sleep(1)
            for shift in range(8):
                oled.shift_display(right=True, count=1)
                sleep(1)
            for shift in range(8):
                oled.shift_display(right=False, count=1)
                sleep(1)
            for shift in range(8):
                oled.shift_display(right=True, count=1)
                sleep(1)
    
    
        else:
            ad = random.choice(ads)
            if ad != lastDisplay:
                footer = 'Hack My Derby!'
    
                if lastDisplay:
                    oled.chompit()
                else:
                    oled.clear_display()
    
                oled.set_pos(0,0)
                oled.shift_display(right=True, count=16)
                oled.write_string(ad.center(16))
                oled.shift_display(right=False, count=16)
                sleep(1)
                oled.set_pos(1,0)
                oled.write_string(footer.center(16))
                lastDisplay = ad
                adLoopCount = adLoopCount + 1

def partyMode():
    sch=2
    oled.clear_display()
    for col in range(16):
        oled.set_pos(1,col)

        if sch == 2 or sch == 3:
            oled.write_raw_data(sch)
        else:
            oled.write_string(sch)

        if sch == 2:
            sch = 3
        elif sch == 3:
            sch = " "
        else:
            sch = 2
    for count in range(20):
        oled.set_pos(0,0)
        oled.write_raw_data(5)
        oled.set_pos(0,3)
        oled.write_raw_data(4)
        oled.set_pos(0,6)
        oled.write_raw_data(5)
        oled.set_pos(0,10)
        oled.write_raw_data(4)
        oled.set_pos(0,14)
        oled.write_raw_data(5)
        sleep(0.5)
        oled.set_pos(0,0)
        oled.write_raw_data(4)
        oled.set_pos(0,3)
        oled.write_raw_data(5)
        oled.set_pos(0,6)
        oled.write_raw_data(4)
        oled.set_pos(0,10)
        oled.write_raw_data(5)
        oled.set_pos(0,14)
        oled.write_raw_data(4)
        sleep(0.5)



    for col in range(16):
        oled.set_pos(0,col)
        oled.write_string(" ")

    for col in [10,3,6,4,8,9,12,4,13,3,15,8]:
        oled.set_pos(0,col)
        oled.write_raw_data(5)
        sleep(0.5)
        oled.set_pos(0,col)
        oled.write_raw_data(4)
        sleep(0.5)
        oled.set_pos(0,col)
        oled.write_string(" ")

    for col in range(16):
        oled.set_pos(0,col)
        oled.write_string(" ")

    oled.set_pos(0,0)
    display = "D E R B Y  C O N"
    oled.write_string(display.center(16), typeomatic_delay=0.5)



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

def oledDisplay(msgType, message):
    # Displays to th oled, doesn't bother if the message hasnt changed.
    global lastDisplay
    #print "Message is %s and lastDisplay is %s" % (message,lastDisplay)
    if msgType == 'p':
        header = 'Pwned!:'
    elif msgType == 'h':
        header = 'Recent host:'

    if message != lastDisplay:
        #print "Upating display"
#        lcd.home()
#        lcd.clear()
#        #lcd.autoscroll()
#        #lcd.setCursor(2,1)
#        lcd.message('%s' % (message))
        if lastDisplay:
            oled.chompit()
        else:
            oled.clear_display()

        oled.shift_display(right=True, count=16)
        oled.set_pos(0,0)
        oled.write_string(header)
        oled.shift_display(right=False, count=16)
        oled.set_pos(1,0)
        tdelay = 0.1
        oled.write_string(message.center(16), typeomatic_delay=tdelay)
        

        lastDisplay = message
    #else:
    #    print "Did not update display"

def getSSID():
    f = '/etc/hostapd/hostapd.conf'
    global ownerTwitter
    search = open(f)
    for line in search:
        line = line.rstrip()
        if re.match('^ssid', line) is not None:
           ssid = line.split('=')[1]
    if 'Alpha' in ssid:
        ownerTwitter = '@gangrif'
    elif 'Beta' in ssid:
        ownerTwitter = '@SunkThought'

    return(ssid)

    
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
            oledDisplay('p',mostRecentPwn[0])
        elif mostRecentHost:
            if displayingHost and count > '0':
                count = count - 1
            elif displayingHost and count <= '0':
                displayingHost = None
            else:
            #print "OLED: %s" % (mostRecentHost[0])
                oledDisplay('h',mostRecentHost[0])
                displayingHost = '1'
                count = dhcpRecentTimer / sleepCount 
        else:
            #print "OLED: %s" % (advertise())
            #oledDisplay(advertise())
            advertise()

        sleep(sleepCount)


if __name__ == '__main__':
    main()

