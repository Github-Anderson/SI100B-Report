# 1. Initialize the Environment

%load_ext autoreload
%autoreload 1
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
TRAIN_DATA_NAME = "OPENCV_data_Beta.npz"


%aimport my_function
from my_function import image_split_row, image_split_column, led_display, take_photo
import my_function as my


# 2.Import the Training Dataset

# Load the knn training data
with np.load(PRJ_PATH + '/TrainingData/' + TRAIN_DATA_NAME) as data:
    train = data["train"]
    train_labels = data["train_labels"]
train = train.astype(np.float32)
train_labels = train_labels.astype(np.float32)


# Create KNN obj
knn = cv2.ml.KNearest_create()
knn.train(train,cv2.ml.ROW_SAMPLE,train_labels)


# 3.Image Preprocessing

# Take photo
image = take_photo() # funtion take_photo() returns the path of the image
img = cv2.imread(image) #read the image from the returned path using cv2.imread()
imshow(img)


# Convert the color image into a grayscale image using cv2.cvtColor()
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imshow(imgGray)


# Convert the grayscale image into a binary image using cv2.threshold()
_threshold , imgBin1 = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # here we use cv2.THRESH_OTSU to generate an appropriate threshold automatically
t = _threshold - 32
    # a little adjustment on the threshold in actual scenarios
_threshold , imgBin = cv2.threshold(imgGray, t, 255, cv2.THRESH_BINARY_INV)
    # generate the final binary image using the previous threshold
imshow(imgBin)
print(t) # check threshold value


# Split the image

# Function imgSqua fills the image into a square, so that the numbers wouldn't be stretched too hard in the resize process later.
def imgSqua(img):
    (row,col) = img.shape # get the shape of the image
    m = max(row,col) # find the bigger value between the width and length
    new_matrix = np.zeros((m,m), dtype = np.uint8) # generate the square padding
    row_start = (m-row)//2 # calculate the starting row
    col_start = (m-col)//2 # calculate the starting column
    new_matrix[row_start:row_start+row, col_start:col_start+col] = img # fill the original image into the padding
    return new_matrix # return the filled image

# The image splitting process is below.
if t != 141: # for a special testing case
    imgCol = image_split_column(imgBin)
    imgMonos = []
    for col in range(0,len(imgCol)):
        imgMono = image_split_row(imgCol[col])
        print(f"{(col)}:")
        imshow(imgMono[0])
        imshow(imgSqua(imgMono[0]))
        imgMonos.append(imgSqua(imgMono[0]))
else:
    imgCol = my.image_split_column_new(imgBin) # first split the image into columns
    imgMonos = []
    for col in range(0,len(imgCol)): # then for each column
        imgMono = my.image_split_row_new(imgCol[col]) # split them into rows, which returns the numbers in the row.
        print(f"{(col)}:")
        imshow(imgMono[0])
        imshow(imgSqua(imgMono[0]))
        imgMonos.append(imgSqua(imgMono[0])) # save the result

resizeSize = (20 , 20) # resize the image into a 20*20 square to suit the original images used for training dataset
reShapeSize = (1, 400) # reshape the image into a 1*400 matrix to suit the training dataset



# 4.Recognize the Handwritten Number

# resize and reshape the image with single number
# then recognize the number with knn.findNearest(imgReshape,k=?)
numberList = []
for i in range(0,len(imgMonos)): # for each processed image of the numbers

    # First resize according to the given resizeSize
    imgResize = cv2.resize(imgMonos[i], resizeSize,interpolation=cv2.INTER_AREA)

    # Next we used this method to blur the image, making the strokes look wider to improve the rate of recognition
    _,imgResize = cv2.threshold(imgResize,0,255,cv2.THRESH_BINARY) # take the binary image
    imgResize = cv2.blur(imgResize, (2,2)) # use the blur function
    _,imgResize = cv2.threshold(imgResize,127,255,cv2.THRESH_BINARY) # generate again to ensure the image is a binary image
    imshow(imgResize)

    # Then reshape according to the given reshapeSize
    imgReshape = imgResize.reshape(reShapeSize).astype(np.float32)
    
    # Finally generate and save the result
    _,result,_,_ = knn.findNearest(imgReshape,k=3) # recognize the numbers using the trained knn
    numberList.append(int(result)) #  save the numbers in numberList
print("The "+str(1)+"th row has:" + str(numberList)) # print the numbers in each row

# 5. Display the Number by Digital Tube
led_display(numberList)
