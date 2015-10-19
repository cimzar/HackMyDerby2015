#!/usr/bin/env python

# A script that just telnet's in order to give attackers something to look for.

import sys
import telnetlib
import time
from time import sleep
import random
import os 

HOST = "10.42.0.11"
PORT = "4000"
user = "hackme"
password = "fluffster"
svcpass = "fluffy69"
codeFile = "/derby/gate4/code"


def getCode():
    # Gets a code from codeFile 
    if os.path.isfile(codeFile):
        with open(codeFile,"r") as f:
            data = f.read()
        readCode = data.strip()
        return readCode

tn = telnetlib.Telnet(HOST, PORT)
tn.read_until('By what name do you wish to be known? ')
tn.write(user+ "\r")
tn.read_until("Password: ")
tn.write(password+ "\r")
tn.read_until("*** PRESS RETURN:")
tn.write("\r")
tn.read_until("Make your choice:")
tn.write("1\r")
tn.read_until("> ")
if tn.expect(["password"], 3600)[1] != -1:
    if random.randint(1,3) == 1:
        tn.write("say Funny you should ask.\r")
        tn.read_until("> ")
        passMsg = "say its %s" % svcpass
        tn.write(passMsg + "\r")
        tn.read_until("> ")
        sleep(10)
        codeMsg = "say and since you asked: %s \r" % getCode()
        tn.write(codeMsg)
        tn.read_until("> ")
        sleep(5)
        tn.write("say Seek ye the ring bearer \r")
    else:
        tn.write("say Why does everyone ask me for my password!\r")
        sleep(10)

tn.write("say Crap, I think i see the boss coming!  BBL!\r")
sleep(2)
tn.write("quit\r")
tn.read_until("Make your choice:")
tn.write("0\r")
tn.close

