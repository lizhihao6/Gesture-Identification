from Adafruit_I2C import Adafruit_I2C
import time


class FDC2214:


    def __init__(self):

        try:

            i2c = Adafruit_I2C(0x2a)
            self.i2c = i2c
            config_reg = i2c.readU16(0x1a)
        
            if( hex(config_reg) != "0x114"):
                    # ROUNCT_CH
                    i2c.write16(0x08, 0xfb34)
                    i2c.write16(0x09, 0xfb34)
                    i2c.write16(0x0a, 0xfb34)
                    i2c.write16(0x0b, 0xfb34)
                
                    # SETTLECOUNT
                    i2c.write16(0x10, 0x1b00)
                    i2c.write16(0x11, 0x1b00)
                    i2c.write16(0x12, 0x1b00)
                    i2c.write16(0x13, 0x1b00)

                    # CLOCK_DIVIDERS
                    i2c.write16(0x14, 0x0220)
                    i2c.write16(0x15, 0x0220)
                    i2c.write16(0x16, 0x0220)
                    i2c.write16(0x17, 0x0220)

                    # DRIVE_CURRENT
                    i2c.write16(0x1e, 0x0078)
                    i2c.write16(0x1f, 0x0078)
                    i2c.write16(0x20, 0x0078)
                    i2c.write16(0x21, 0x0078)

                    # ERROR_CONFIG
                    i2c.write16(0x19, 0x0000)

                    # MUX_CONFIG
                    i2c.write16(0x1b, 0x0dc2)

                    #CONFIG
                    i2c.write16(0x1a, 0x0114)

        except:
            
            with open("error.txt","a+") as file:
                file.write("Failed to init FDC2214\n")


    def read_reg(self,addr):

        i2c = self.i2c
        reg_d = i2c.readU16(addr)
        reg_h = hex(reg_d)
        if(len(reg_h)<6):
            temp = "0x"
            for i in range(6-len(reg_h)):
                temp += "0"
            for i in range(len(reg_h)-2):
                temp += reg_h[-(i+1)]
                reg_h = temp
        reg_rev = reg_h[4] + reg_h[5] + reg_h[2] + reg_h[3]
        return reg_rev


    def read_data(self, channel):

        msg = ""
        lsg = ""
        if(channel == 0):
            msg = self.read_reg(0x00)
            lsg = self.read_reg(0x01)
        elif(channel == 1):
            msg = self.read_reg(0x02)
            lsg = self.read_reg(0x03)
        elif(channel == 2):
            msg = self.read_reg(0x04)
            lsg = self.read_reg(0x05)
        else:
            msg = self.read_reg(0x06)
            lsg = self.read_reg(0x07) 
        data_h = "0x" + msg + lsg
        return(int(data_h,16))

    
    def get_all_data(self):

        data_list = [0.0 for i in range(4)]
        for i in range(20):
            for j in range(4):
                data_list[j] += self.read_data(j)
            time.sleep(0.01)
        temp_list = []
        for i in range(4):
            temp =  232021045.248 *20 / data_list[i]
            temp_list.append( temp**2)
        return temp_list


    def get_data_1(self):

        data = 0.0
        for i in range(20):
            data += self.read_data(1)
            time.sleep(0.01)
        return [data]


    def get_distance(self):

        data = 0.0
        for i in range(10):
            data += self.read_data(4)
            time.sleep(0.01)
        return data*2


    def differ(self, a, b):

        c = []
        if(len(a)!=len(b)):
            print("Warnning! a != b")
        for i in range(len(a)):
            c.append(a[i]-b[i])
        return c


    def knn(self, train, test):
        
        length_list = []
        for i in range(len(train)):
            length = 0.0
            for j in range(len(test)):
                length += (train[i][j] - test[j])**2
            length_list.append(length)
        
        _length_list = []
        sum_length = 0.0
        for i in range(len(length_list)):
            _length_list.append(length_list[0]/length_list[i])
            sum_length += length_list[0]/length_list[i]

        p_list = []
        for length in _length_list:
            p_list.append(length/sum_length)
        
        return p_list

