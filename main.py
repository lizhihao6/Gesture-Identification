from BUTTON import BUTTON
import Adafruit_BBIO.GPIO as GPIO
from FDC2214 import FDC2214
from OLED import OLED
import time
import pickle
import math

rst = False

def set_rst(channel):
    global rst
    rst = True


class GAME:


    def __init__(self):
        
        self.button = BUTTON()
        self.fdc2214 = FDC2214()
        self.oled = OLED()
        self.base_data = []
        self.rps_data = []
        self.rps_label = []
        self.finger_data = []
        self.finger_label = []
        self.distance = 0.0
        GPIO.add_event_detect("P8_14", GPIO.RISING, callback = set_rst, bouncetime=200)


    def menu(self):
        
        while(True):
            self.oled.draw_image("/root/image/menu.png",0)
            key = self.button.wait_button_click()
            if (key == 3):
                self.rps_menu()
            elif (key == 2):
                self.finger_menu()
            elif (key == 1):
                self.adventure_menu()
            else:
                time.sleep(0.1)


    def adventure_menu(self):

        self.oled.draw_image("/root/image/adventure_menu.png",0)
        key = self.button.wait_button_click()
        if (key == 3):
            self.train_once()
        elif (key == 2):
            self.two_site()
        elif (key == 1):
            self.free_distance()
        else:        
            return


    def rps_menu(self):
        
        self.oled.draw_image("/root/image/rps_menu.png",0)
        key = self.button.wait_button_click()
        if (key == 3):
            self.rock_paper_scissors_notrain()
        elif (key == 2):
            self.rock_paper_scissors_train()
        else:
            return
    

    def finger_menu(self):
        
        self.oled.draw_image("/root/image/rps_menu.png",0)
        key = self.button.wait_button_click()
        if (key == 3):
            self.finger_notrain()
        elif (key == 2):
            self.finger_train()
        else:
            return


    def train_once(self):

        self.base_data = self.fdc2214.get_all_data()
        five = self.train_rps_data("paper", 32)
        if(five==False):
            return
        
        one = [0.0,0.0,five[3]*0.2]
        two = [0.0,0.0,five[3]*0.5]
        three = [0.0,0.0,five[3]*0.7]
        four = [five[0],0.0,five[3]*0.8]
        five = [five[0],five[1]*0.8,five[3]*0.8]
        rock = [0.0,0.0,0.0]

        train_data = [one,two,three,four,five,rock]
        train_label = ["one","two","three","four","paper","rock"]

        global rst
        rst = False
        
        while(True):

            if(rst):
                rst = False
                break

            data = self.get_differ(1)
            p_list = self.fdc2214.knn(train_data,[data[0],data[1],data[3]])
            index = p_list.index(max(p_list))
            label = train_label[index]
            self.oled.draw_image("/root/image/" + label + ".png",52)
            time.sleep(0.5)


    def two_site(self):

        self.base_data = self.get_finger_data()
        finger_data = []
        finger_label = ["one","one","two","two","three","three","four","four","five"]

        for label in finger_label:
            data = self.train_finger_data(label,52)
            if (data == False):
                return
            finger_data.append(data)

        self.finger_data = finger_data
        self.finger_label = finger_label

        pickle.dump(self.finger_data, open('/root/data/finger_data.pkl', 'wb'))
        pickle.dump(self.finger_label, open('/root/data/finger_label.pkl', 'wb'))

        last_label = ""
        global rst
        rst = False

        while(True):

            if(rst):
                rst = False
                break

            data = self.fdc2214.differ(self.get_finger_data(),self.base_data)
            p_list = self.fdc2214.knn(self.finger_data,data)
            label = self.finger_label[p_list.index(max(p_list))]

            if(label != last_label):
                last_label = label
                self.oled.draw_image("/root/image/" + label + ".png",52)
        

    def free_distance(self):
    
        self.base_data = self.fdc2214.get_all_data()
        rps_data = []
        rps_label = ["scissors","rock","paper"]

        for label in rps_label:

            data = self.train_rps_data(label,32)
            if (data == False):
                return
            rps_data.append(data)

        rps_data_f = []
        for label in rps_label:
            data = self.train_rps_data(label,32)
            if (data == False):
                return
            rps_data_f.append(data)
        
        last_label = ""
        global rst
        rst = False

        while(True):

            if(rst):
                rst = False
                break

            data = self.get_differ(1)

            k = data[2]/rps_data[0][2]
            _data = [data[0]/k, data[1]/k,data[2]/k,data[3]/k]
            p_list = self.fdc2214.knn(rps_data, _data)

            k_f = rps_data_f[0][2]/data[2]
            _data = [data[0]*k_f, data[1]*k_f,data[2]*k_f,data[3]*k_f]
            p_list_f = self.fdc2214.knn(rps_data_f, _data)

            print(k,k_f)

            _p_list = [ k*p_list[0] + k_f*p_list_f[0], k*p_list[1] + k_f*p_list_f[1], k*p_list[2] + k_f*p_list_f[2] ]
            label = rps_label[_p_list.index(max(_p_list))]
            if(label != last_label):
                last_label = label
                self.oled.draw_image("/root/image/" + label + ".png",32)


    def rock_paper_scissors_notrain(self):

        self.base_data = self.fdc2214.get_all_data()
        self.rps_data = pickle.load(open('/root/data/rps_data.pkl', 'rb'))
        self.rps_label = pickle.load(open('/root/data/rps_label.pkl', 'rb'))

        last_label = ""
        global rst
        rst = False

        while(True):

            if(rst):
                rst = False
                break

            data = self.get_differ(1)
            p_list = self.fdc2214.knn(self.rps_data, data)
            label = self.rps_label[p_list.index(max(p_list))]
            if(label != last_label):
                last_label = label
                self.oled.draw_image("/root/image/" + label + ".png",32)


    def rock_paper_scissors_train(self):
        
        self.base_data = self.fdc2214.get_all_data()
        self.rps_data = []
        self.rps_label = ["scissors","rock","paper"]

        for label in self.rps_label:
            data = self.train_rps_data(label,32)
            if (data == False):
                return
            self.rps_data.append(data)
        
        self.rps_data.append(  [ -0.2 for i in range( len(self.rps_data[0]) ) ]  )
        self.rps_label.append("no_hand")

        pickle.dump(self.rps_data, open('/root/data/rps_data.pkl', 'wb'))
        pickle.dump(self.rps_label, open('/root/data/rps_label.pkl', 'wb'))

        last_label = ""
        global rst
        rst = False

        while(True):

            if(rst):
                rst = False
                break

            data = self.get_differ(1)
            p_list = self.fdc2214.knn(self.rps_data, data)
            label = self.rps_label[p_list.index(max(p_list))]
            if(label != last_label):
                print(data)
                last_label = label
                self.oled.draw_image("/root/image/" + label + ".png",32)


    def finger_notrain(self):

        self.base_data = self.get_finger_data()
        self.finger_data = pickle.load(open('/root/data/finger_data.pkl', 'rb'))
        self.finger_label = pickle.load(open('/root/data/finger_label.pkl', 'rb'))

        last_label = ""
        global rst
        rst = False

        while(True):

            if(rst):
                rst = False
                break

            data = self.fdc2214.differ(self.base_data,self.get_finger_data())
            p_list = self.test_finger(data)
            label = self.finger_label[p_list.index(max(p_list))]
            if(label != last_label):
                last_label = label
                self.oled.draw_image("/root/image/" + label + ".png",52)


    def finger_train(self): 

        self.base_data = self.get_finger_data()
        finger_data = []
        finger_label = ["one","two","three","three","four","five"]

        for label in finger_label:
            data = self.train_finger_data(label,52)
            if (data == False):
                return
            finger_data.append(data)

        finger_data.append([-0.01 for i in range(len(finger_data[0]))])
        finger_label.append("no_hand")

        self.finger_data = finger_data
        self.finger_label = finger_label

        pickle.dump(self.finger_data, open('/root/data/finger_data.pkl', 'wb'))
        pickle.dump(self.finger_label, open('/root/data/finger_label.pkl', 'wb'))

        last_label = ""
        global rst
        rst = False

        while(True):

            if(rst):
                rst = False
                break

            data = self.fdc2214.differ(self.get_finger_data(),self.base_data)
            p_list = self.fdc2214.knn(self.finger_data,data)
            label = self.finger_label[p_list.index(max(p_list))]
                    
            if(label != last_label):
                last_label = label
                self.oled.draw_image("/root/image/" + label + ".png",52)


    def get_differ(self, k):

        data = self.fdc2214.get_all_data()
        _data = []
        for d in data:
            _data.append(d*k)
        return (self.fdc2214.differ(self.base_data,_data))


    def get_div(self,a,b):
    
        c = []
        for i in range(len(a)):
            c.append(a[i]/b[i])
        return c


    def train_rps_data(self, label, bias):
        self.oled.draw_image("/root/image/" + label + ".png",bias)
        key = self.button.wait_button_click()
        if (key == 3):
            return self.get_differ(1)
        else:
            return False


    def train_finger_data(self, label, bias):
        self.oled.draw_image("/root/image/" + label + ".png",bias)
        key = self.button.wait_button_click()
        if (key == 3):
            return self.fdc2214.differ(self.get_finger_data(),self.base_data)
        else:
            return False

    
    def test_finger(self, data):
         
        if(data[0] > self.finger_data[-2][0]*0.7):
            result =  [0 for i in range(len(self.finger_label))]
            result[-2] = 1
            return result
        elif(data[2] > self.finger_data[-2][2]*0.7):
            result =  [0 for i in range(len(self.finger_label))]
            result[-3] = 1
            return result
        else:
            return(self.fdc2214.knn(self.finger_data,data))


    def get_finger_data(self):

        data =  self.fdc2214.get_all_data()
        return [data[1],data[3],data[0]]

    
    def get_mid(self,a,b,c):
        
        max_num = max(a,b,c)
        min_num = min(a,b,c)
        temp = [a,b,c]
        temp.remove(max_num)
        temp.remove(min_num)
        return temp[0]


def start():
    
    game = GAME()
    # base_data = sqrt(game.fdc2214.get_all_data())
    # raw_input()
    # bias = sqrt(game.fdc2214.get_all_data())
    # while(True):
    #     data = sqrt(game.fdc2214.get_all_data())
    #     temp = []
    #     for i in range(4):
    #         temp.append((data[i] - base_data[i])/(bias[i]-base_data[i]))
    #     print(temp)    
    #     time.sleep(0.6)
    game.menu()
    # game.free_distance()


if __name__ == '__main__':
    
    start()
