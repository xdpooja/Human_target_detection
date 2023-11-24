from tkinter import *
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
width, height = 800, 600
detection_threshold = 0.3
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
app = Tk()
app.title("Code Clan")
app.iconbitmap('cctv.ico')
app.configure(background='black')
app.geometry('800x600')
label_widget = Label(app)
label_widget.grid(row = 0, column = 1, pady = 1)
running = False

def start():
    global running
    running = True
def stop():
    global running
    running = False

def tracking():
    if running :
        _, frame = cap.read()
        tracking1 = model.track(frame, persist=True, classes=0, tracker = 'bytetrack.yaml')
        frame_ = tracking1[0].plot()
        opencv_image = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGBA)
        captured_image = Image.fromarray(opencv_image)
        photo_image = ImageTk.PhotoImage(image=captured_image)
        label_widget.photo_image = photo_image
        label_widget.configure(image=photo_image)
        label_widget.after(10, tracking)
     

def entryfield():
	global a
	entry = Entry(app, textvariable= 'Enter the label ID')
	entry.grid(row = 1, column = 1, pady = 2)
	a = int(entry.get())
	button1.configure(text= 'ok',command= lambda : [stop(),custom_tracking()])

    
cap2 = cv2.VideoCapture(0)

def custom_tracking() :
    cap.release()
    _, frame1 = cap2.read()
    results1 = model.track(frame1, persist=True, classes = 0, tracker = 'bytetrack.yaml')
    for result in results1:
        for r in result.boxes.data.tolist(): 
            x1, y1, x2, y2,id, score, class_id = r
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)
            id = int(id)
            print(r)
            if id == a:                            
                cv2.rectangle(frame1, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame1, str(id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.imshow('frame2', frame1)
            
                new_frames = results1[0].plot()
                opencv_image = cv2.cvtColor(new_frames, cv2.COLOR_BGR2RGBA)
                captured_image = Image.fromarray(opencv_image)
                photo_image = ImageTk.PhotoImage(image=captured_image)
                label_widget.photo_image = photo_image
                label_widget.configure(image=photo_image)
                label_widget.after(10, custom_tracking)

button1 = Button(app, text="Start Tracking", command=lambda:[start(),tracking(), entryfield()])
button1.grid(row = 2, column = 1, pady = 2)

app.mainloop()
