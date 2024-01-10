# SI100B-Report

## Team members and Division of Work

### Team members

ZhangZhi Xiong  (熊章智)

TianNi Yang        (杨天倪)

YiXuan Chen	   (陈逸轩)

### Division of Work

## Text

### Main Content of the Project

#### Part 1: Some Preparations

The Project "hand-written number recognition" is  realized through hardwares and program. As for the hardware, we use a Raspberry Pi model '3b'  as the remote control and a Pi camera attached to it. As for the program, the language we use is Python, and we will use the KNN algorithm in OpenCV, which is a typical method in the field of Image Processing. Besides these two parts, to realize the interaction between the hardwares and the real world, we have to build a circuit with LED light and LED digital tube added, so as to better tell us the moment of taking photos and the result of the algorithm. 

First of all, the most important thing is to understand how to operate the Raspberry Pi. We know that the Raspberry is a little computer with no screen or input device. As for the first stage, we will build a ***Remote Desktop*** through ***VNC***, in order to make it easy for us to write in programs and run our codes through our own computer. This may seem to be a little bit weird, but in fact, our computer only plays the role of displayer, and the running of codes is actually processed in the Raspberry Pi.  

To realize this, we have to assign an IP to the usb interface in order to connect the Raspberry with the computer, since that this operation puts two devices into one LAN.   After that, all we have to do is to open the VNC app and initiate the connection. Through these operations, we can manipulate the Raspberry Pi through the remote desktop on our own computer. 

#### Part 2: The Establishment of the Training Set

KNN algorithm requires training data. But before that, we must know how to process our pictures. The photos taken is colorful, but this is not what we want. First, we have to change our colorful pictures into the gray one. Picture is actually a matrix, containing the RGB information of every pixel. But we don't want the RGB colors, all we want is to use a gray level value to represent the pixel. Using the algorithm in the library OpenCV, it is easy to realize this:

````python 
grayImg = cv2.cvtColor(src, code)
# code can be  `cv2.COLOR_BGR2GRAY`,
# `cv2.COLOR_BGR2RGB`,`cv2.COLOR_BGR2HSV`.
````

After that, the colorful picture is converted to a ***gray scale picture***. To us the converted picture to generate training data set, we have to provide samples which contain the picture of each digit and the attached label to tell the true answer.  To split the picture into samples like that, we use the ***numpy*** library to realize that. With labels attached, the data are finally set up, ready to be used in the KNN algorithm. 

````python
# number detected related
import cv2
import os
import numpy as np
import math
from lib import imshow
import random
# get the project path
PRJ_PATH = os.getcwd()
# OPENCV_data.npz
TRAIN_DATA_NAME = "OPENCV_data.npz"
img = cv2.imread(PRJ_PATH+"/DigitsLib/digits.png")
grayImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cells = [np.hsplit(row,100) for row in np.vsplit(grayImg,50)]
cells = np.array(cells)
# Training set
train = cells[:,:].reshape(-1,400).astype(np.float32)
# Testing set
test = cells[:,50:100].reshape(-1,400).astype(np.float32)
k = np.arange(10) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# Training set
train_labels = np.repeat(k, 5 * 100)[:,np.newaxis]
# Testing set
test_labels = np.repeat(k,5 * 50)[:,np.newaxis]
knn = cv2.ml.KNearest_create()
knn.train(train ,cv2.ml.ROW_SAMPLE , train_labels)
# Testing the training model
ret, result, neighbors, dist = knn.findNearest(test,k = 3)
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct/result.size
print(f"{accuracy * 100: 0.02f}%")
# As for this case, when k=1, the accuracy would be 100%
# When k=3, the accuracy would be 97.56%

# Save your training model
fileName = os.path.join(PRJ_PATH, "TrainingData", TRAIN_DATA_NAME)
np.savez(fileName, train = train, train_labels = train_labels)
````

Pay special attention to the grammar when splitting the picture.

### Presentation & Result of the Project

### Problems Encountered and Solutions

#### Problem 01: Recognition rate

The first problem we've encountered is how to raise the recognition rate. In the first few times, we've found the recognition rate is too low, around **30~40%**, since the expectation is about 90%. 

#### Problem 02: Camera initialization

When attempting to initialize the newly installed camera on the Raspberry Pi, it consistently presents an ***'Failed to enable connection: Out of resources'*** error. Despite trying several solutions, the issue persists.

#### Problem 03: Camera preview

After writing the `camera.start_preview()` code, the Raspberry Pi, which should have initiated the camera preview, remained unresponsive without any error messages. Nevertheless, it executed the subsequent code without issues.

### Thoughts and Inspirations

