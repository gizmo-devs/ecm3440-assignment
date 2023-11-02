
import numpy as np
import cv2 as cv
import sys
import tkinter
from tkinter import *
from PIL import Image, ImageTk

width, height = 500, 400

class Camera():
    def __init__(self):
        self.feed = None
    
    def __del__(self):
        self.feed.release()
    
    def initalise(self):
        self.feed = cv.VideoCapture(0)
        self.feed.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.feed.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    def show(self):
        _, frame = self.feed.read()
        frame = cv.flip(frame, 1)
        cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        res = ImageTk.PhotoImage(image=img)
        update_image(res)
        imagelab.after(10, self.show)

def initCamera():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    
    cam = Camera()
    cam.initalise()
    cam.show()

def update_image(image):
    imagelab.configure(image=image)
    imagelab.image=image

def OrigionalButClick(input) :
    iproc=0
    colour_converted = cv.cvtColor(input,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    update_image(test)

##def main():
##    pass

def GreyButClick(input) :
    iproc=1
    gray = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
    colour_converted = cv.cvtColor(gray,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    update_image(test)

def SobelButClick(input) :
    iproc=2
    gsobel = cv.Sobel(input,cv.CV_8U,1,0,ksize=3)
    colour_converted = cv.cvtColor(gsobel,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    update_image(test)

def CannyButClick(input) :
    iproc=3
    edges = cv.Canny(input,100,200)
    colour_converted = cv.cvtColor(edges,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    update_image(test)

def BlurButClick(input) :
    iproc=4
    blur2 = cv.blur(input,(5,5))
    colour_converted = cv.cvtColor(blur2,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    update_image(test)

if __name__ == '__main__':
   ## main()

    iproc = 0
    mainwindow = tkinter.Tk()
    mainwindow.title("Jimmy Test Form")
    mainwindow.geometry("800x600")

    mainwindow.bind('<Escape>', lambda e: mainwindow.quit()) 

    imageframe = tkinter.Frame(mainwindow,width=790,height=590,
                               highlightbackground="black",highlightthickness=2)
    imageframe.pack(expand=True)

    YOURIMAGE ="helperfiles/img.jpg"
    ## DONT USE TOO BIG AN IMAGE 500 x 400 is OK
    
    img = cv.imread(cv.samples.findFile(YOURIMAGE))

    if img is None:
        sys.exit("Could not read the image.")

    colour_converted = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    imagelab = tkinter.Label(imageframe, image=test)

    imagelab.grid(row=0, column=0, padx=2, pady=2)

    buttonframe = tkinter.Frame(mainwindow,width=790,height=200,
                               highlightbackground="black",highlightthickness=2)
    buttonframe.pack(expand=True)
    buttonOrig = tkinter.Button(buttonframe,text='Origional',font=20, command = lambda: OrigionalButClick(img) )
    buttonOrig.grid(row=0,column=0)

    buttonGrey = tkinter.Button(buttonframe,text='Grey',font=20, command = lambda: GreyButClick(img))
    buttonGrey.grid(row=0,column=1)

    buttonSobel = tkinter.Button(buttonframe,text='Sobel',font=20,command = lambda: SobelButClick(img))
    buttonSobel.grid(row=0,column=2)

    buttonBlur = tkinter.Button(buttonframe,text='Blur',font=20,command = lambda: BlurButClick(img))
    buttonBlur.grid(row=0,column=3)

    buttonCanny = tkinter.Button(buttonframe,text='Canny',font=20,command = lambda: CannyButClick(img))
    buttonCanny.grid(row=0,column=4)

    buttonCam = tkinter.Button(buttonframe,text='Camera',font=20,command = initCamera)
    buttonCam.grid(row=1,column=0)

    mainwindow.mainloop()