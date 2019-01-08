import cv2
#cascade classifier object
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
img = cv2.imread("news.jpg")
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #converts rbg image into grayscale

#search for the cascade classifier(xml) in our image and return coordinates of face in the image
#finds a rectangle, where face begins, and height and width

faces = face_cascade.detectMultiScale(gray_img,
scaleFactor = 1.1,
minNeighbors = 5)  #if something goes wrong, play with these
#scaleFactor is the percentage by which python descreases the scale of the image for the next search
#this time decreases by 5% (1.05) and researches for bigger faces, until it goes to the final size
#smaller value = higher accuracy
#minNeighbors means how many neigbours to search around the window

for x, y, w, h in faces:
    img = cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0), 3)  #upper left and lower right corner, color and width of rect

print(type(faces))
print(faces)  #array with 4 values, num of column, row, width,height

resized = cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))  #img and tuple of width and height
cv2.imshow("Gray",resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
