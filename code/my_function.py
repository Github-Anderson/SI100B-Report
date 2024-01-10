# General purpose
import os
import numpy as np
from time import sleep
import time


# GPIO related
import RPi.GPIO as GPIO

# camera related
from picamera import PiCamera, Color
# GPIO mode: GPIO.BOARD, GPIO.BCM
GPIO.setmode(GPIO.BOARD)
mode = GPIO.getmode()
# Close GPIO warning
GPIO.setwarnings(False)
# get the project path
PRJ_PATH = os.getcwd()


def image_split_column(img:np.ndarray)->list:
    """
    Function description: Splite the image by column. 
    Tips:
    1. Calculate the number of elements with a value of 255 in each column.
    2. When the number of 255 changes from zero to non-zero, it indicates the beginning of the digits area. Use startList to record the starting column index.
    3. When the number of 255 changes from non-zero to zero, it indicates the end of the digits area. Use endList to recorder the end column index.
    4. Use flag to represent the current state, outside or inside the digits area.
    
    :param img: input image to be splited by column.
    :return: output image after splited by column. It is a list, but its elements are np.ndarray.
    """
    
    # find out the number of columns in the original image
    # create a list to record the number of elements with a value of 255 in each column
    column = img.shape[1]
    columnHist = np.zeros(column)
    
    # initialize the variables
    flag = 0
    startList = []
    endList = []
    
    
    ### write your codes here ###
    #############################
    # step1:
    # count the number of elements with a value of 255 in each column and record it in columnHist
    # record the location where the the number of 255 changes in startList and endList
    # record the status with flag
    for i in (range(column-1)):
        if 255 not in img[:,i]:
            if 255 in img[:,i+1]:
                startList.append(i)
        if 255 in img[:,i]:
            if 255 not in img[:,i+1]:
                endList.append(i+1)
    
                   
    # step 2:
    # following the startList and the endList, split the digits area from the original image.
    # there maybe several areas. recorder the areas in imgList and return imgList.
    imgList = [img[:,startList[i]-15:endList[i]+15] for i in range(len(startList))]
    
    
    
            
    
    ret = imgList
    return ret



def image_split_row(img:np.ndarray)->list:
    """
    Function description: Splite the image by row. 
    Tips:
    1. Calculate the number of elements with a value of 255 in each row.
    2. When the number of 255 changes from zero to non-zero, it indicates the beginning of the digits area. Use startList to record the starting row index.
    3. When the number of 255 changes from non-zero to zero, it indicates the end of the digits area. Use endList to recorder the end row index.
    4. Use flag to represent the current state, outside or inside the digits area.
    
    :param img: input image to be splited by row.
    :return: output image after splited by row. It is a list, but its elements are np.ndarray.
    """
    
    # find out the number of rows in the original image
    # create a list to record the number of elements with a value of 255 in each row
    row = img.shape[0]
    rowHist = np.zeros(row)
    
    # initialize the variables
    flag = 0
    startList = []
    endList = [] 
    
    
    ### write your codes here ###
    #############################
    # step1:
    # count the number of elements with a value of 255 in each row and record it in rowHist
    # record the location where the the number of 255 changes in startList and endList
    # record the status with flag
    for i in (range(row-1)):
        if 255 not in img[i,:]:
            if 255 in img[i+1,:]:
                startList.append(i)
        if 255 in img[i,:]:
            if 255 not in img[i+1,:]:
                endList.append(i+1)
    
    
    
    
        
    # step 2:
    # following the startList and the endList, split the digits area from the original image.
    # there maybe several areas. recorder the areas in imgList and return imgList.    
    imgList = [img[startList[i]-15:endList[i]+15,:] for i in range(len(startList))]     
    
    
     
    
    ret = imgList
    return ret


def led_display(numList:list)->None:
    
    """
    Function description: Build a digital tube display circuit on the breadboard. Display the result with the digital tube.
    Tips:
    1.The GPIO mode we used is GPIO.BOARD. 
    2.The digital tube is common anode. Use GPIO port to input high level for digital tube power pin.
    3. After the LED lamp pin of the digital tube is connected to the GPIO pin, the corresponding relationship can be confirmed by lighting the led one by one.
    4. Check "function introduction.xlsx" for GPIO functions.
    
    :para numList: input numbers in list to be displayed.
    :return: None
    """

    ### write your codes here ###
    #############################
    # step 1:
    # Clarify the relationship between led pins and GPIO pins
    # Set the GPIO pins to GPIO.OUT mode and give them the right output
    
    GPIO.setmode(GPIO.BOARD)
    out_para = GPIO.HIGH
  
    #GPIO.setup(12, GPIO.OUT, out_para)
    #GPIO.setup(13, GPIO.OUT, out_para)
    #GPIO.setup(16, GPIO.OUT, out_para)
    #GPIO.setup(18, GPIO.OUT, out_para)
    #GPIO.setup(29, GPIO.OUT, out_para)
    #GPIO.setup(31, GPIO.OUT, out_para)
    #GPIO.setup(35, GPIO.OUT, out_para)
    #GPIO.setup(37, GPIO.OUT, out_para)
    
    # step 2:
    # Clarify the led composition of each number
    a = 31
    b = 29
    c = 16
    d = 13
    e = 12
    f = 35
    g = 37
    dp = 18
    seg = [12,13,16,18,29,31,35,37]
    for segment in seg:
        GPIO.setup(segment,GPIO.OUT)
        GPIO.output(segment, True)
    num0 = [a,b,c,d,e,f]
    num1 = [b,c]
    num2 = [a,b,g,e,d]
    num3 = [a,b,g,c,d]
    num4 = [f,g,b,c]
    num5 = [a,f,g,c,d]
    num6 = [a,f,g,c,d,e]
    num7 = [a,b,c]
    num8 = [a,b,c,d,e,f,g]
    num9 = [a,b,c,d,f,g]
    n_list = [num0,num1,num2,num3,num4,num5,num6,num7,num8,num9]
    
        
    # step 3:
    # Display the numbers in the list one by one
    # Display every number for 1 second
    # Wait two seconds when displaying different lines
    
    for ele in numList:
        for dig in n_list[ele]:
            GPIO.output(dig, GPIO.LOW)
        time.sleep(1)
        for dig in n_list[ele]:
            GPIO.output(dig, GPIO.HIGH)
        time.sleep(1)
    
    GPIO.cleanup() 
    ret = None
    return ret


def take_photo()->str:
    """
    Function description: Build the camera control circuit on the breadboard. After pressing the control button, the shooting indicator(led light) lights up and the camera takes a picture.
    Tips:
    1. Use the 3.3v and GND pins on the Raspberry Pi as the power and ground of the circuit.
    2. Use the GPIO port as a signal line to sense the occurrence of key events. Set the correct GPIO mode
    3. Create a camera obj and wait for a button press to take a photo.
    4. Save the picture to /UserData/.
    5. Clean the camera.
    
    :para
    :return: a string which contains the picture location
    """

    ### write your codes here ###
    #############################
    # step 1: 
    #set a GPIO as an input channel for detecting
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(40,GPIO.OUT)
        
    
    
    
    # step 2: 
    # create the camera obj and wait for a button to take a photo
    # recorder the saving path
    # clear the camera
    with PiCamera() as camera:
             
        camera.start_preview()
        while True:  
            
            if GPIO.input(7) == 1:
                GPIO.output(40,GPIO.HIGH)
                sleep(1)
                GPIO.output(40,GPIO.LOW)                      
               
                
                sleep(1)
                camera.stop_preview()
                filename = 'photo.jpg'
                camera.capture(PRJ_PATH + filename)
                   
                GPIO.cleanup()
                camera.close()
                break
    # step3:
    # return the saving path
    
    
    
    
    ret = PRJ_PATH + filename
    return ret