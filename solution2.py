import httplib, urllib
import sys
import tty
import termios
import logging
import thread
import time
import fcntl
import os
import RPi.GPIO as GPIO
import nfc
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from Adafruit_CharLCDPlate2 import Adafruit_CharLCDPlate2

emptyLine = "                "
lcd = Adafruit_CharLCDPlate()
lcd.begin(16, 2)
lcd.clear()
lcd.message("Welcome.\nStarting...")
lcd.backlight(lcd.ON)
time.sleep(2)
def sendPOST (message):

    params = urllib.urlencode({'@number': message, '@type': 'issue', '@action': 'show'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("bugs.python.org")
    conn.request("POST", "", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()
    return data

def getch():
    fd = sys.stdin.fileno()

    oldattr = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while True:
            try:
                c = sys.stdin.read(1)
            except IOError:
                pass
            else:
                return c
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldattr)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



GPIO.cleanup()

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    while True:
        msg = ""
        ch = "x"
        index = 0
        maxLength = 16;
        lcd.clear()
        print "0 card - 1 key"
        lcd.message("0 card - 1 key")

        #wait for the user selection: 0 for card reader - 1 for key a password
        while (ch != '0') and (ch != "1"):

            ch = getch()

        lcd.clear();
        lcd.blink();

        if (ch == "0"):
            print "Waiting for card"
            lcd.message("Waiting for card\n")
            data = nfc.readNfc()
            lcd.message("Authenticating..\n")
            response = sendPOST(data)
            lcd.message(response)
            #other actions will follow once you know what to do once the autenthication process suceeded

        if (ch == "1"):
            lcd.clear()
            lcd.message("Type password:\n")
            while (ord(ch) != 10):
                ch = getch()
                msg = msg + ch
                lcd.message("*")
                print msg

            lcd.noBlink()
            lcd.clear()
            lcd.message("Authenticating..\n")
            response = sendPOST(msg)
            lcd.message(response)
            print response


        print "Restarting from scratch in 5 seconds..."
        time.sleep (5)


except KeyboardInterrupt:
    GPIO.cleanup()
    lcd.clear()
    lcd.noBlink()
    lcd.backlight(lcd.OFF)
    pass
