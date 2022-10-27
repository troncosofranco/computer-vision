#Impor Modules
import cv2
import pickle
import cvzone
import numpy as np
 
# Video feed
cap = cv2.VideoCapture('Video.mp4')
 
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

#Rectangle dimensions
width, height = 105, 52 

 
#Check function
def checkParkingSpace(imgPro):
    spaceCounter = 0
 
    for pos in posList:
        x, y = pos
 
        imgCrop = imgPro[y:y + height, x:x + width]
        
        count = cv2.countNonZero(imgCrop)
 
 
        if count < 600:
            color = (0, 255, 0) #Green: Empty
            thickness = 1
            spaceCounter += 1
        else:
            color = (0, 0, 255) # Red
            thickness = 1

        #Rectangle plot
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=1, offset=0, colorR=color)
    
    #counter text
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (200, 50), scale=2,
                           thickness=2, offset=5, colorR=(0,200,0))

#Main function
while True:
 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()

    #Gray matrix in rectangle
    #convert an image from one color space to another
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    #Low-pass filter such as guassian blur to reduce high frequency components as follows
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1) #3x3 filter

    #Where 100 is threshold that divides the pixel space , hence all pixel values smaller than 100 are set to 0 and all above 100 are set to 255.
    #The THRESH_BINARY specifies method used for thresholding
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    #Matrix
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
 
    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    
    cv2.waitKey(10)