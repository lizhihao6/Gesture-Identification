import Adafruit_BBIO.GPIO as GPIO
import time

class BUTTON:


    def __init__(self):

        try:
            GPIO.setup("P8_14", GPIO.IN)
            GPIO.setup("P8_16", GPIO.IN)
            GPIO.setup("P8_18", GPIO.IN)
            GPIO.setup("P8_19", GPIO.IN)
        
        except:
            with open("error.txt","a+") as file:
                file.write("Failed to init Button\n")
        

    def wait_button_click(self):

        key = 0

        while(True):
    
            if(GPIO.input("P8_14")):
                key = 0
                break
            if(GPIO.input("P8_16")):
                key = 1
                break
            if(GPIO.input("P8_18")):
                key = 2
                break
            if(GPIO.input("P8_19")):
                key = 3
                break

            time.sleep(0.01)
        
        return key


    #def start_rst_update(self):
        
        


    #def stop_rst_update(self):

        #GPIO.remove_event_detect("P8_14")






if __name__ == '__main__':

    button = BUTTON()
    print("wait a key")
    key = button.wait_button_click()
    print(key)