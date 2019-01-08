import cv2, time, pandas
from datetime import datetime


first_frame = None  #nothing assigned
status_list = [None, None]  #None so the index would not be out of range when searching for [-2]
times = []
df = pandas.DataFrame(columns = ["Start","End"])

video = cv2.VideoCapture(0)  #if a number = loading vid from camera number 0,1,2... if a title, already existing video

while True:
    check, frame = video.read()  #bool and numpy array
    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21), 0)  #to remove noise, increase accuracy in calculation of difference
    #tuple - w and h of Gaussian kernel, parameter of blurriness
    #+ standard deviation is 0 and I don't know why

    if first_frame is None:
        first_frame = gray
        continue  #continue to the beginning of loop

    delta_frame = cv2.absdiff(first_frame,gray)

    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]  #image, limit of pixel value, color to turn it into if pix more than 30
    #and also the method, THRESH_BINARY, there are more. threshold method returns a tuple with 2 values - one suggest a value for threshold & the
    #actual frame that is returned from the threshold method. for THRESH_BINARY we only need the second one, hence [1]

    thresh_delta = cv2.dilate(thresh_delta, None, iterations = 2)  #kernel array is second parameter, for sophisticated stuff

    #find contours stores in tuple,and draw contours draws contours in an image
    (_,cnts,_) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #copy so we don't modify the thresh_delta
    #second is the method that draws external line of contours, and the last one is approximation method... what :(


    for c in cnts:
        if cv2.contourArea(c) < 10000:  #if area has less than 1000 pixels go back
            continue
        status = 1  #when pyhton finds the area
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
    status_list.append(status)

    status_list = status_list[-2:]  #to only show alst two items

    #to track the changes from 0 to 1 and 1 to 0, two last indices of list
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())

    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())


    cv2.imshow("Gray frame", gray)
    cv2.imshow("Delta frame", delta_frame)
    cv2.imshow("Threshold frame", thresh_delta)
    cv2.imshow("Color frame", frame)
    key = cv2.waitKey(1)  #how does this work?

    if key == ord('q'):  #Return the Unicode code point for a one-character string.
        if status == 1:
            times.append(datetime.now())  #to add the last exit time
        break

print(status_list)
#print(times)  #no exit time for the last enterance

for i in range(0,len(times),2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index = True)
#good job Ardit!

df.to_csv("Times.csv")

video.release()  #stop
cv2.destroyAllWindows()
