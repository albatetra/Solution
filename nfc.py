import MFRC522

def readNfc():
    reading = True
    MIFAREReader = MFRC522.MFRC522()
    while reading:
        

        #while continue_reading:
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        #if status == MIFAREReader.MI_OK:
        #    print("Card detected")

        (status,backData) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            MIFAREReader.AntennaOff()
            reading=False
            return str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])
