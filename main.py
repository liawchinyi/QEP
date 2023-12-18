'''

Main Module: Espressif ESP32-WROOM-32U (ESP32-D0WD) (240MHz, Dual-Core, 32-Bit LX6 Microprocessor)
Digital Lock Box Program
18 December 2023

'''
# ======================================================================================
# Import required MicroPython libraries.
# ======================================================================================

import machine
from machine import ADC, Pin, Timer, SPI, RTC, UART
import time
from time import ticks_us, ticks_cpu, sleep, sleep_us, sleep_ms
import sys
import select
p = select.poll()
p.register(sys.stdin)
import gc  # gc 模块 garbage collector to free up memory
import ubinascii
from micropython import const
from usys import stdin
from uselect import poll

import os
import re

gc.enable()  # 启用自动垃圾回收 Enable garable collector
# Register the standard input so we can read keyboard presses.
keyboard = poll()
keyboard.register(stdin)

# ======================================================================================
# Define Variables
# ======================================================================================

var1 = 1 # global variable
varA = 2 # global variable
varB = 3 # global variable
varC = 4 # global variable

cmdstr = '' # input command string
key = 0
TEST_c = '\0'
Sel_Task_Global = 0  # global variable to set the task to be executed
USB_input = '\0\0\0\0\0'

#Initialize the onboard LED as ouput
ledG = Pin(2, Pin.OUT)
ledR = Pin(4, Pin.OUT)
#Initialize timer_one. Used for toggeling the LED
timer_one = Timer(0)
#Initialize timer_two. Used for changing the State
timer_two = Timer(1)
#Initialize state variable of timer. Used for changing the State
state = 1
toggle = 1

# ======================================================================================
# Define Some Functional Tasks 
# ======================================================================================
def BlinkLED(timer_one):
    global toggle
    if toggle == 1:
        ledG.value(0)
        ledR.value(1)
        toggle = 0
    else:
        ledG.value(1)
        ledR.value(0)
        toggle = 1
# ======================================================================================
# Define Some Functional Tasks
# ======================================================================================    
def ChangeState(timer_two):
    global state
    
    if state == 1:
     # 100mS Timer initialization   
     timer_one.init(freq=10, mode=Timer.PERIODIC, callback=BlinkLED)
     state = state+1
    elif state == 2:
     # 250mS Timer initialization
     timer_one.init(freq=4, mode=Timer.PERIODIC, callback=BlinkLED)
     state = state+1
    elif state == 3:
     # 1000mS Timer initialization
     timer_one.init(freq=1, mode=Timer.PERIODIC, callback=BlinkLED)
     state = 1
    else:
      # Default state
      # 100mS Timer initialization
      state = 1
      timer_one.init(freq=10, mode=Timer.PERIODIC, callback=BlinkLED)

# Initialize the timer one for first time
timer_one.init(freq=10, mode=Timer.PERIODIC, callback=BlinkLED)
state = state+1

# Initialize the timer two to change states at 20 seconds interval
timer_two.init(freq=0.05, mode=Timer.PERIODIC, callback=ChangeState)

print('MicroPython Booting \n\r')

# --------------------------------------------------------------------------------------
# getchar from keyboard function
# --------------------------------------------------------------------------------------
def isData():
    global uart, cmdstr, key
    # return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
    # Check if a key has been pressed.
    flags = p.poll(0)[0]
    if flags :
        key = sys.stdin.read(1)
        keynum = ord(key) # convert ascii to number

        if keynum != 10 and key != '\r':
            cmdstr = cmdstr + key
            return False
        else :
            cmdstr = cmdstr + '\n\r'
            return True           

# ======================================================================================
# command decoder 指令输入解码器
# ======================================================================================
def GetUserCommand(): # 
    global Sel_Task_Global, USB_input, cmdstr, TEST_c  
    exec_once_flag = False
    while True:
        if isData() == True :
            TEST_c = cmdstr[0]
            if TEST_c == '$' or TEST_c == '!' or TEST_c == '@':  # x1b is ESC '\x1b'
                USB_input = cmdstr[1:9]
                TEST_c = '\0'

                if (exec_once_flag == False): #                

                    Sel_Task_Global = ord(cmdstr[1]) # Decode command from input and returns an integer                
                 
                    exec_once_flag = True # inform task in lists to execute
                    tic = time.ticks_us() # start time for calculating elapsed time later 

                    cmdstr = "" # clear str

                else :
                    print("Unknown command " + str(Sel_Task_Global) + "\n\r")

            else :
                cmdstr = ""

        if (Sel_Task_Global == 0 and exec_once_flag == True):
            print('Enter Command > ', end="")
            exec_once_flag = False

        yield None
        
# --------------------------------------------------------------------------------------
# example function 
# --------------------------------------------------------------------------------------
def empty_task1(): # '!1E1' '!1F1'
    global Sel_Task_Global    
    while True : 
        if Sel_Task_Global == 49 : # '!1' 
            print("empty_task1 press CTRL-C to stop ")
            Sel_Task_Global = 0
        yield None
# --------------------------------------------------------------------------------------
# example function 
# --------------------------------------------------------------------------------------
def empty_task2(): # '!1E1' '!1F1'
    global Sel_Task_Global    
    while True : 
        if Sel_Task_Global == 50 : # '!2' 
            print("empty_task2 press CTRL-C to stop ")
            Sel_Task_Global = 0
        yield None
# --------------------------------------------------------------------------------------
# example function 
# --------------------------------------------------------------------------------------
def empty_task3(): # '!1E1' '!1F1'
    global Sel_Task_Global
    while True : 
        if Sel_Task_Global == 51 : # '!3'
            print("empty_task3 press CTRL-C to stop ")
            Sel_Task_Global = 0
        yield None
# --------------------------------------------------------------------------------------
# function 
# --------------------------------------------------------------------------------------        
def what(var, locals=locals()):
    for name, value in list(locals.items()):
        if value is var:
            return name        
# --------------------------------------------------------------------------------------
# function 
# --------------------------------------------------------------------------------------
def set_var_task4(): # '!1E1' '!1F1'
    global Sel_Task_Global,var1,varA,varB,varC
    while True : 
        if Sel_Task_Global == 33 : # "!!" Perform Sofware Reboot
            machine.reset()

        if Sel_Task_Global == 70 : # 'F' Set var "!F12345"
            integers  = USB_input[1:6]
            strings = [str(integer) for integer in integers]
            a_string = "". join(strings)
            var1 = int(a_string)
            print('var1 : '+ str(var1)+ ' set\n\r')     
            Sel_Task_Global = 0
            
        if Sel_Task_Global == 83 : # 'S' 
            if USB_input[1] == 'A' :   # 'S' Set var "!SA12345"                  
                integers  = USB_input[2:7]
                strings = [str(integer) for integer in integers]
                a_string = "". join(strings)
                varA = int(a_string)
                print('varA : '+ str(varA)+ ' set\n\r')

            if USB_input[1] == 'B' :   # 'S' Set var "!SB12345"                       
                integers  = USB_input[2:7]
                strings = [str(integer) for integer in integers]
                a_string = "". join(strings)
                varB = int(a_string)
                print('varB : '+ str(varB)+ ' set\n\r')
                
            if USB_input[1] == 'C' :   # 'S' Set var "!SC123.5"                      
                integers  = USB_input[2:7]
                strings = [str(integer) for integer in integers]
                a_string = "". join(strings)
                varC = float(a_string)
                print('varC : '+ str(varC)+ ' set\n\r')
            Sel_Task_Global = 0

        if Sel_Task_Global == 76 : # 'L' list variables                   
            for name, value in globals().copy().items():
                if name.startswith("var"):
                    print(name, value)
        
            Sel_Task_Global = 0

        yield None
        
# ---------------------------------------------------------------------------
# USB串口输入指令模式 Type command “!1\n” or “!2\n” etc
# ---------------------------------------------------------------------------
task_list = { # Descending priority
            0: GetUserCommand,                 # Always First One Executed
            1: empty_task1,                    # “!1\n” example
            2: empty_task2,                    # “!2\n” example
            3: empty_task3,                    # “!3\n” example
            4: set_var_task4,                  # “!S1234\n” example
            }

# --------------------------------------------------------------------------------------
# Get the function from task_list dictionary
# --------------------------------------------------------------------------------------
def get_func(argument):
    func = task_list.get(argument, "nothing") # Execute the function
    return func()

exec_list = []         	# 空指令模块列表
for task in task_list:  # task loop here
    exec_list.append(get_func(task)) # 创建指令模块列表

# --------------------------------------------------------------------------------------
# Initialise the hspi interface
# --------------------------------------------------------------------------------------
import AD7793
hspi = SPI(1, 10000000, polarity=1, phase=1, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
ADC = AD7793.ADC7793(hspi,1)

# --------------------------------------------------------------------------------------
print('Memory : {} bytes free, {} bytes alloc'.format(gc.mem_free(), gc.mem_alloc()) + '\n\r')
print('Enter Command > ', end="")
while True:
    
    for task in exec_list:     # loop all the tasks in the list
        next(task) 
        
    gc.collect() # free up memory
