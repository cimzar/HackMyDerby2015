#!/usr/bin/env python
import os



right = 'kmfdm'
wrong = 'rammstein'
codeFile = '/derby/code'
flagFile = '/var/openssh/tmp/pwn'

def getCode():
    # Gets a code from codeFile 
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
    ans = raw_input("Name a german industrial band\nwith an anti-political theme,\nand an Ultra-Heavy Beat:\n")
    
    ans = ans.strip()
    
    if ans.lower() == right:
        code = getCode()
        print "No pity for the Majority."
        display = raw_input("What would you like to display:\n(this will be truncated at 16 characters)\n")
        display = display[:16]
        writePwn(display) 
        print "And, for your trouble: %s" % (code)
    elif ans.lower() == wrong:
        print 'Not quite.\n    Hint: You probably haven\'t \n\theard them on the radio.'
    else:
        print "no"
    

if __name__ == '__main__':
    main()

