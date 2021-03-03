import cv2, time, pandas
from datetime import datetime

first_frame=None
status_list=[None,None] #trick
times=[]
df=pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0) #video in

while True:
    check, frame = video.read() #check - check is the video capturing, frame - first frame from the camera
    status=0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #converting into gray
    gray = cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.countourArea(contour) < 10000: # if contour < 1000px continue
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour) #draw the recntangle around countour
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255), 3) #add rectangle to frames
    status_list.append(status)

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Capturing", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key=cv2.waitKey(1) #new image every milisecond

    if key==ord('q'): #if q is entered then loop breaks
        if status==1:
            times.append(datetime.now())
        break

for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows