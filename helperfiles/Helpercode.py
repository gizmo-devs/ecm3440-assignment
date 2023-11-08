
import numpy as np
import cv2 as cv
import sys
import tkinter
from tkinter import *
from PIL import Image, ImageTk



def OrigionalButClick() :
    iproc=0
    colour_converted = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    imagelab.configure(image=test)
    imagelab.image=test

##def main():
##    pass

def GreyButClick() :
    iproc=1
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    colour_converted = cv.cvtColor(gray,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    imagelab.configure(image=test)
    imagelab.image=test

def SobelButClick() :
    iproc=2
    gsobel = cv.Sobel(img,cv.CV_8U,1,0,ksize=3)
    colour_converted = cv.cvtColor(gsobel,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    imagelab.configure(image=test)
    imagelab.image=test

def CannyButClick() :
    iproc=3
    edges = cv.Canny(img,100,200)
    colour_converted = cv.cvtColor(edges,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    imagelab.configure(image=test)
    imagelab.image=test

def BlurButClick() :
    iproc=4
    blur2 = cv.blur(img,(5,5))
    colour_converted = cv.cvtColor(blur2,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    imagelab.configure(image=test)
    imagelab.image=test

if __name__ == '__main__':
   ## main()

    iproc = 0
    mainwindow = tkinter.Tk()
    mainwindow.title("Jimmy Test Form")
    mainwindow.geometry("800x600")
    imageframe = tkinter.Frame(mainwindow,width=790,height=590,
                               highlightbackground="black",highlightthickness=2)
    imageframe.pack(expand=True)

    YOURIMAGE ="src/sample-greyson.jpg"
    ## DONT USE TOO BIG AN IMAGE 500 x 400 is OK
    
    img = cv.imread(cv.samples.findFile(YOURIMAGE))

    if img is None:
        sys.exit("Could not read the image.")

    colour_converted = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    pil_Image = Image.fromarray(colour_converted)
    test = ImageTk.PhotoImage(pil_Image)
    imagelab = tkinter.Label(imageframe,image=test)

    imagelab.grid(row=0,column=0,padx=2,pady=2)



    buttonframe = tkinter.Frame(mainwindow,width=790,height=200,
                               highlightbackground="black",highlightthickness=2)
    buttonframe.pack(expand=True)
    buttonOrig = tkinter.Button(buttonframe,text='Origional',font=20, command = OrigionalButClick)
    buttonOrig.grid(row=0,column=0)

    buttonGrey = tkinter.Button(buttonframe,text='Grey',font=20, command = GreyButClick)
    buttonGrey.grid(row=0,column=1)

    buttonSobel = tkinter.Button(buttonframe,text='Sobel',font=20,command = SobelButClick)
    buttonSobel.grid(row=0,column=2)

    buttonBlur = tkinter.Button(buttonframe,text='Blur',font=20,command = BlurButClick)
    buttonBlur.grid(row=0,column=3)

    buttonCanny = tkinter.Button(buttonframe,text='Canny',font=20,command = CannyButClick)
    buttonCanny.grid(row=0,column=4)




    mainwindow.mainloop()