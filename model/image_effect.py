import cv2 as cv
import numpy as np

import os

mask2x2 = np.array([[1,1],
                    [1,1]])

mask3x3 = np.array([[1,1,1],
                            [1,1,1],
                            [1,1,1]])

mask5x5 = np.array([[1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1]])

def apply_effect(app, input):
    if 5 in app.effect:
        if not app.facedetection:

            app.convolutionMask = mask3x3
            ## pass in the image path and the effect or use the defaults
            
            
            app.facedetection == True
            
        gray=cv.cvtColor(input,cv.COLOR_BGR2GRAY)
        faces=app.faceCascade.detectMultiScale(gray, 1.2,5)
        drawonme = input.copy()
        tempROI = input.copy() ## make it acopy for it case it is not there
        nw, nh = (20, 20) 
        for(x,y,w,h) in faces:
            tempROI = input[y:y+h, x:x+w]
            height, width = tempROI.shape[:2]

            # Resize input to "pixelated" size
            temp = cv.resize(tempROI, (nw, nh), interpolation=cv.INTER_LINEAR)

            # Initialize output image
            tempROI = cv.resize(temp, (width, height), interpolation=cv.INTER_NEAREST)
            # tempROI = cv.filter2D(tempROI,-1,convolutionMask5x5)

            drawonme[y:y+h, x:x+w] = tempROI
            cv.rectangle(drawonme, (x, y), (x + w, y + h), (200, 200, 200), 4)

        input = drawonme

    if 1 in app.effect:
        app.facedetection=False
        # blur
        input = cv.blur(input,(5,5))
        # return cv.cvtColor(blur,cv.COLOR_BGR2RGB)
    if 2 in app.effect:
        app.facedetection=False
        # grey
        input = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
        # return cv.cvtColor(gray,cv.COLOR_BGR2RGB)
    if 3 in app.effect:
        app.facedetection=False
        # Canny
        input = cv.Canny(input,100,200)
        # return cv.cvtColor(edges,cv.COLOR_BGR2RGB)
    if 4 in app.effect:
        app.facedetection=False
        # Sobel
        input = cv.Sobel(input,cv.CV_8U,1,0,ksize=3)
        # return cv.cvtColor(gsobel,cv.COLOR_BGR2RGB)
    
    return cv.cvtColor(input, cv.COLOR_BGR2RGB)