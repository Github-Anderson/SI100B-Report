# SI100B-Report

## Team members and Division of Work

### Team members

> ZhangZhi Xiong  (熊章智)
>
> TianNi Yang        (杨天倪)
>
> YiXuan Chen	   (陈逸轩)
>

### Division of Work

## Text

### Main Content of the Project

#### Part 1: Some Preparations

The Project "hand-written number recognition" is  realized through hardwares and program. As for the hardware, we use a Raspberry Pi 3B  as the remote control and a Pi camera attached to it. As for the program, the language we use is Python, and we will use the KNN algorithm in OpenCV, which is a typical method in the field of Image Processing. Besides these two parts, to realize the interaction between the hardwares and the real world, we have to build a circuit with LED light and LED digital tube added, so as to better tell us the moment of taking photos and the result of the algorithm. 

First of all, the most important thing is to understand how to operate the Raspberry Pi. We know that the Raspberry is a little computer with no screen or input device. As for the first stage, we will build a **Remote Desktop** through **VNC**, in order to make it easy for us to write in programs and run our codes through our own computer. This may seem to be a little bit weird, but in fact, our computer only plays the role of displayer, and the running of codes is actually processed in the Raspberry Pi.  

To realize this, we have to assign an IP to the usb interface in order to connect the Raspberry with the computer, since that this operation puts two devices into one LAN.   After that, all we have to do is to open the VNC app and initiate the connection. Through these operations, we can manipulate the Raspberry Pi through the remote desktop on our own computer. 

#### Part 2: The Establishment of the Training Set



### Presentation & Result of the Project

### Problems Encountered and Solutions

#### Problem 01: Recognition rate

- **Description:** The initial challenge we faced was improving the recognition rate. During the first few attempts, we observed a low recognition rate of approximately **30~40%**, which fell far short of our target of around 90%.

- **Solution:** We used several methods, including cropping to retain suitable margins, adjusting binary thresholds, and applying blur filters, which are shown in the following code:

```python
# Applying blur filters
imgResize = cv2.blur(imgResize, (2,2))
_,imgResize = cv2.threshold(imgResize,127,255,cv2.THRESH_BINARY)
```

#### Problem 02: Camera initialization

- **Description:** When attempting to initialize the newly installed camera on the Raspberry Pi, it consistently presents an ***'Failed to enable connection: Out of resources'*** error. Despite trying several solutions, the issue persists.
- **Solution:** We eventually diagnosed the issue by running code `vcgencmd get_camera` in the terminal, which revealed `supported=1 detected=0`, means that the problem stemmed from poor camera connections, preventing the initialization process. Once we powered down and reconnected the camera, the issue was resolved.

#### Problem 03: Camera preview

- **Description:** After writing the `camera.start_preview()` code, the Raspberry Pi, which should have initiated the camera preview, remained unresponsive without any error messages. Nevertheless, it executed the subsequent code without issues.
- **Solution:** Unfortunately, despite our best efforts, including disabling the VNCServer, the problem persisted. Consequently, we had to rely on blind navigation during the code testing phase.

### Thoughts and Inspirations

