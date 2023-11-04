import cv2 as cv

def apply_effect(app, input):
    if app.effect == 1:
        # blur
        blur = cv.blur(input,(5,5))
        return cv.cvtColor(blur,cv.COLOR_BGR2RGB)
    if app.effect == 2:
        # grey
        gray = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
        return cv.cvtColor(gray,cv.COLOR_BGR2RGB)
    if app.effect == 3:
        # Canny
        edges = cv.Canny(input,100,200)
        return cv.cvtColor(edges,cv.COLOR_BGR2RGB)
    if app.effect == 4:
        # Sobel
        gsobel = cv.Sobel(input,cv.CV_8U,1,0,ksize=3)
        return cv.cvtColor(gsobel,cv.COLOR_BGR2RGB)
    
    return cv.cvtColor(input, cv.COLOR_BGR2RGB)