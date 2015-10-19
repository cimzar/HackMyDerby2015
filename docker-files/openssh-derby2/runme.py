#!/usr/bin/env python
import os
import pwd

uid = pwd.getpwuid( os.getuid() ).pw_uid
right = 'derbycon'
codeFileL1 = '/derby/l1/code'
codeFileL2 = '/derby/l2/code'
#flagFile = '/var/openssh/tmp/pwn'
flagFile = '/derby/pwn'

def getCode(level):
    # Gets a code from codeFile 
    if level == 1:
        codeFile = codeFileL1
    elif level == 2:
        codeFile = codeFileL2

    if os.path.isfile(codeFile):
        with open(codeFile,"r") as f:
            data = f.read()
        readCode = data.strip()
        return readCode

def writePwn(display):
    f = open(flagFile, 'w')
    f.write(display)
    f.close()
    

def main():
    if uid != 0:
        print "That was too easy... %s" % (getCode(1))
    else:
        ans = raw_input("What is the best con on the planent?\n")
    
        ans = ans.strip()
    
        if ans.lower() == right:
            print "You know it."
            display = raw_input("What would you like to display:\n(this will be truncated at 16 characters)\n")
            display = display[:16]
            writePwn(display) 
            print "And, for your trouble: %s" % (getCode(2))
        else:
            print "no"
    

if __name__ == '__main__':
    main()

