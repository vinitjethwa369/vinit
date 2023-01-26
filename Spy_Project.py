import tkinter # use to available graphics tool / use to acees buttons and components
from datetime import datetime
import cv2 # manipualate camera related resources
import pyttsx3 # to prompt in speech
from tkinter import *  # font
from PIL import ImageTk,Image # add image in GUI

def speak(cmd1): # notify the detected movement
    engine = pyttsx3.init('sapi5') #sapi5 microsoft framewowrk.. tect in audio
    engine.say(cmd1) # speaks
    engine.runAndWait()

def record():   # recording function
    cap = cv2.VideoCapture(0)   

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'{datetime.now().strftime("%H-%M-%S")}.mp4', fourcc, 20.0, (640, 480))

    while True: 
        _, frame = cap.read()

        cv2.putText(frame, f'{datetime.now().strftime("%D-%H-%M-%S")}', (50, 50), cv2.FONT_HERSHEY_COMPLEX,
                    0.6, (255, 255, 255), 2)

        out.write(frame)

        cv2.imshow("esc. to stop", frame)

        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

def inout():  

    # to read the capture/turn on the camera on 0 source
    cap = cv2.VideoCapture(0)

    # to read the frame we're using frame1
    _, frame1 = cap.read()

    # for in and out our left right and center initially is false
    left, right, center = False, False, False

    # assigning random value to x
    x = 300

    # to run infinitely
    while True:
        # to detect the motion we need 2 consecutive frames
        _, frame2 = cap.read()

        # to convert into gray scale
        g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # abs diff function need gray scale image and to reduce computation we are using gray scale
        # to calculate the difference we are passing gray scaled frames
        diff = cv2.absdiff(g1, g2)

        # this gray scale is producing color from 0-255 bu wee need 0 or 255 so we have to use thresh
        # the function is source is diff and if the value is less than 30 set it to 0 else grater than 30 set it to 255
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # contour is no ting but the list which returning the rectangle around the motion
        # we are finding contours which we are passing thresh as source and reaming are criteria
        contr, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # to avoid value error of max function no vale in list if motion is not detected
        if len(contr) > 0:
            # to get the max rectangle value use max function which accept list(contr) and on which basis we need
            contr = max(contr, key=cv2.contourArea)

            # accepting rectangles dimensions from contr
            x, y, w, h = cv2.boundingRect(contr)

            # defining rectangle according to given dimensions
            # para         source  cordi  wid hig  color  thik
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # to check our frame is empty or not
        if not left and not right:
            # motion happened in left
            if x < 100:
                left = True
            # motion happened in right
            elif x > 500:
                right = True
        # if value of center is not set yet
        elif left:
            # to set the center value according to left
            if x > 100 and x < 500 and not center:
                center = True
            # to detect the motion from right to left
            if x > 500:
                if center:
                    speak("motion happened from right to left")
                    # if once it activates for another turn we have to disable it to active agin
                    center = False
                    left = False
                else:
                    right = True
                    left = False

        # if value of center is not set yet
        elif right:
            # to set the center value according to right
            if x > 100 and x < 500 and not center:
                center = True;
            # to detect the motion from left to right
            if x < 100:
                if center:
                    speak("motion happened from left to right")
                    # if once it activates for another turn we have to disable it to active agin
                    center = False
                    right = False
                else:
                    left = True
                    right = False

        # to show the video capture(frame 1) on window
        cv2.imshow("window", frame1)

        # if we have to show output to user of threshold image on window 2
        cv2.imshow("window2", thresh)

        # to update the frame 1 to
        _, frame1 = cap.read()

        # to get out from window we're using wait key function which is equal to esc key
        if cv2.waitKey(1) == 27:
            # to release the camera resource
            cap.release()
            # to close all windows
            cv2.destroyAllWindows()
            # to get out from loop
            break
        
def ex():
    exit(0)

top = Tk()

top.geometry("1000x500")
top.title("Spy")

I1= ImageTk.PhotoImage(Image.open('Spy_1.png'))
I2= ImageTk.PhotoImage(Image.open('incognit.png'))
I3= ImageTk.PhotoImage(Image.open('recording.png '))
I4= ImageTk.PhotoImage(Image.open('exit1.png'))

l1 = Label(text="SPY CCTV CAMERA", width=40, height=2, font="Arial,BOLD, 18", )
img = Label(image=I1)
b = Button(top, image=I2, text="InOut          ", command=inout, compound=tkinter.LEFT, highlightthickness=2, bd=1)
b1 = Button(top, image=I3, text="Recording", command=record, compound=tkinter.LEFT, highlightthickness=2, bd=1)
b2 = Button(top, image=I4, text="Exit           ", command=ex, compound=tkinter.LEFT, highlightthickness=2, bd=1)
l1.pack()

img.pack()
b.place(x=570, y=300)
b1.place(x=320, y=300)
b2.place(x=460, y=380)
``
top.mainloop()