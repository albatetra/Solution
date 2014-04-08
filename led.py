
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

emptyLine = "                "
lcd = Adafruit_CharLCDPlate()
lcd.begin(16, 2)
lcd.clear()
lcd.message("LCD LED Test....")
lcd.backlight(lcd.ON)
sleep(2)


lcd.message("Testing Colors")
col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.ON   , lcd.OFF)
for c in col:
    lcd.backlight(c)
    sleep(1)


btn = ((lcd.LEFT, 'Color is\nRed', lcd.RED),
       (lcd.UP, 'Color is\nBlue', lcd.BLUE),
       (lcd.DOWN, 'Color is\nGreen', lcd.GREEN),
       (lcd.RIGHT, 'Color is\nViolet', lcd.VIOLET),
       (lcd.SELECT, '', lcd.ON))


prev = -1

try:
    while True:
        for b in btn:
            if lcd.buttonPressed(b[0]):
                if b is not prev:
                    lcd.clear()
                    lcd.message(b[1])
                    lcd.backlight(b[2])
                    prev = b
                    break
            
except KeyboardInterrupt:
    GPIO.cleanup()
    lcd.clear()
    lcd.noBlink()
    lcd.backlight(lcd.OFF)
    pass
