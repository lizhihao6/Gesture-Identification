# 基于FDC2214电容传感器的手势识别

## 环境
运行环境为Beaglebone Black  

需部署SH1104的驱动文件，或更改OLED.py至合适驱动  

基础IO调用及I2C读写使用Adafruit库

## 文件说明

BUTTON.py   
监测按键输入

FDC2214.py    
传感器初始化，及数据读取，数据预处理，NN算法

OLED.py    
OLED显示屏初始化，调用可直接显示指定路径图片或直接显示文字

main.py    
手势识别的基础算法，和整体流程设计  
包含：猜拳预训练，猜拳训练，划拳预训练，划拳训练，隔空识别猜拳，一次训练识别划拳，划拳正反面识别。

setup.py    
防止刚开机后i2c初始化未完成就进入系统
