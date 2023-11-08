
import cv2 as cv
import numpy as np
from PIL import Image, ImageTk
#import getopt

inimage = ''

effect = 6 ## Use this in a case statement to select the effect This could be passed in as an argument
effectvalue = -999

convolutionMask2x2 = np.array([[1,1],
                               [1,1]])

convolutionMask3x3 = np.array([[1,1,1],
                               [1,1,1],
                               [1,1,1]])

convolutionMask5x5 = np.array([[1,1,1,1,1],
                               [1,1,1,1,1],
                               [1,1,1,1,1],
                               [1,1,1,1,1],
                               [1,1,1,1,1]])

convolutionMask5x5 = convolutionMask2x2
## pass in the image path and the effect or use the defaults
cascadePath = "helperfiles/haarcascade_frontalface_alt.xml"
faceCascade = cv.CascadeClassifier(cascadePath)

print('Creating Video Capture .. Please wait')
cam = cv.VideoCapture(0)
while True:
    ret, im =cam.read()
    ## here we can adjust the image
    gray=cv.cvtColor(im,cv.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    drawonme = im.copy()
    tempROI = im.copy() ## make it acopy for it case it is not there
    nw, nh = (20, 20) 
    for(x,y,w,h) in faces:
        tempROI = im[y:y+h, x:x+w]
        height, width = tempROI.shape[:2]

        # Resize input to "pixelated" size
        temp = cv.resize(tempROI, (nw, nh), interpolation=cv.INTER_LINEAR)

        # Initialize output image
        tempROI = cv.resize(temp, (width, height), interpolation=cv.INTER_NEAREST)
        # tempROI = cv.filter2D(tempROI,-1,convolutionMask5x5)

        ##  tempROI = cv.Canny(tempROI,50,120)
        ##  tempROI = cv.cvtColor(tempROI,cv.COLOR_GRAY2BGR)
        drawonme[y:y+h, x:x+w] = tempROI
        cv.rectangle(drawonme, (x, y), (x + w, y + h), (0, 260, 0), 4)

    canny = cv.Canny(im,5,100) ## not uses - if you want to edge detect the image
    
    # filtered3 = cv.filter2D(im,-1,convolutionMask5x5 /25) # not used - if you want to Blur
	## here we can adjust the image	
    # cv.imshow('Origional',im)
    cv.imshow('Adjusted',drawonme)
    ## cv.imshow('Adjusted',filtered3) # NOT USED
    ## cv.imshow('Adjusted',canny) #NOT USED


   #PRESS the q Keyboard key to quit
    if cv.waitKey(10) & 0xFF==ord('q'):
        break ## break the while TRUE
cam.release()
cv.destroyAllWindows()


