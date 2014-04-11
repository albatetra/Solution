import httplib, urllib
import sys
import tty
import termios
import logging
import thread
import time
import fcntl
import os
import atexit
import RPi.GPIO as GPIO
from select import select
import curses
import nfc
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from Adafruit_CharLCDPlate2 import Adafruit_CharLCDPlate2

emptyLine = "                "
lcd1 = Adafruit_CharLCDPlate()
lcd2 = Adafruit_CharLCDPlate2()
lcd1.begin(20, 4)
lcd2.begin(20, 4);
lcd1.clear()
lcd2.clear()
lcd1.message("Welcome.\nStarting...")
lcd1.backlight(lcd.ON)

GPIO.cleanup()
##@GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

global col = [lcd1.RED , lcd1.YELLOW, lcd1.GREEN, lcd1.TEAL,lcd1.BLUE, lcd1.VIOLET, lcd1.ON , lcd1.OFF]
global indexCol
indexCol = 0


def toggleLed():
    global indexCol
    indexCol = indexCol + 1
    if indexCol == 6:
        indexCol = 0
    lcd1.backlight(col[indexCol])
    lcd2.backlight(col[indexCol])
    print indexCol



class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []



print "Welcome. \nStarting..."
time.sleep(2)

global cardNumber
cardNumber = -1
insertedPassword = -1

def readCard():
    global cardNumber
    print "Thread is running..."
    while(1):
        if (cardNumber == -1):
            cardNumber = nfc.readNfc()
            time.sleep(5)


#def readCard2():

#    GPIO.setup(31, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#    global cardNumber
#    print "Thread is running..."
#    while(1):
#       if (cardNumber == -1):
#            if (GPIO.input(31) == 0):
#                print "X DETECTED"
#                cardNumber = 999
#                time.sleep(5)

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

def gotcha():
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



try:


    while True:
        msg = ""
        ch = "x"
        index = 0
        maxLength = 16;
        lcd1.clear()
        #print "0 card - 1 key"
        #//lcd1.message("0 card - 1 key")

        #wait for the user selection: 0 for card reader - 1 for key a password
        #while (ch != '0') and (ch != "1"):

        #    ch = getch()

        #lcd1.clear();
        lcd1.blink()

        # Card Reader Thread start here.
        # Will keep reading card even during an insert pin procedure
        # !!! start Thread Read Card !!!



        print "Waiting for card"
        lcd1.message("Waiting for card\n")
        data = nfc.readNfc()
        ##@chaf = gotcha()
        ##@data = 232
        #lcd2.message("Authenticating..\n")
        #response = sendPOST(data)
        #lcd2.message(response)
        #other actions will follow once you know what to do once the autenthication process suceeded

        try:
            thread.start_new_thread(readCard2,())
        except Exception as errtxt:
            print errtxt
            pass



        lcd1.clear()
        lcd1.message("Type PIN:\n")

        print "Type PIN:"
        kb = KBHit()

        while (1):

          if kb.kbhit():
                ch = kb.getch()
                if ord(ch) == 10:
                    break
                msg = msg + ch
                lcd1.message("*")
                ##@print "*"



          if cardNumber != -1:
            msg = ""
            lcd1.clear()
            data = cardNumber
            cardNumber = -1
            lcd1.message("Type PIN:\n")
            ##@print "Type PIN:\n"
            lcd2.clear
            lcd2.message("Other card passed")




        lcd1.noBlink()
        lcd1.clear()
        lcd2.clear()
        lcd2.message("Authenticating..\n")
        if msg=="117979":
            toggleLed()
            lcd2.message("Changing LED color")
        else:
            response = sendPOST(msg)
            print "Card Number:",data
            print "PIN Number:",msg
            lcd2.message(response)
            print response


        print "Restarting from scratch in 5 seconds..."
        time.sleep (5)


except KeyboardInterrupt:
    GPIO.cleanup()
    lcd1.clear()
    lcd1.noBlink()
    lcd1.backlight(lcd.OFF)
    lcd2.clear()
    lcd2.noBlink()
    lcd2.backlight(lcd.OFF)

    pass



