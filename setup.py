import Adafruit_BBIO.GPIO as GPIO
import time
import main


def set_rst(channel):
    global rst
    rst = True 

if __name__ == '__main__':
    
    global rst
    rst = False

    GPIO.setup("P8_16", GPIO.IN)
    GPIO.add_event_detect("P8_16", GPIO.RISING, callback = set_rst, bouncetime=200)

    while(True):
        if(rst):
            rst = False
            main.start()
            break