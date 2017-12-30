from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2


cap0=cv2.VideoCapture(0)
cap0.set(3,160)
cap0.set(4,120)

cap1=cv2.VideoCapture(1)
cap1.set(3,160)
cap1.set(4,120)
global cX2
global cX1,D
cX1=0
cX2=0;D=0
count=0
while(1):
    ret,img1=cap0.read()
    ret,img2=cap1.read()
    image_blur1 = cv2.GaussianBlur(img1, (7, 7), 0)
    image_blur2 = cv2.GaussianBlur(img2, (7, 7), 0)
    #HSV format of image
    image_blur_hsv1 = cv2.cvtColor(image_blur1, cv2.COLOR_BGR2RGB)
    image_blur_hsv2 = cv2.cvtColor(image_blur2, cv2.COLOR_BGR2RGB)

    #colour grading for cone
    max_orange = np.array([245,136,99])
    min_orange = np.array([150,45,10])

    max_white= np.array([225,224,228])
    min_white=np.array([119,115,136])

    #colour masks, using only orange
    mask11 = cv2.inRange(image_blur_hsv1,min_orange,max_orange)
    mask12 = cv2.inRange(image_blur_hsv1,min_white,max_white)
    mask21 = cv2.inRange(image_blur_hsv2,min_orange,max_orange)
    mask22 = cv2.inRange(image_blur_hsv2,min_white,max_white)

    mask1=mask11+mask12
    mask2=mask21+mask22

    #canny edges
    edged1 = cv2.Canny(mask11, 50, 100)
    edged1 = cv2.dilate(edged1, None, iterations=1)
    edged1 = cv2.erode(edged1, None, iterations=1)
    edged2 = cv2.Canny(mask21, 50, 100)
    edged2 = cv2.dilate(edged2, None, iterations=1)
    edged2 = cv2.erode(edged2, None, iterations=1)

    #contour plays
    _,contours1,_ = cv2.findContours(edged1, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    _,contours2,_ = cv2.findContours(edged2, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours1) and len(contours2))!=0:
        c1 = max(contours1, key = cv2.contourArea)
        M1=cv2.moments(c1)
        if M1["m00"] != 0:
            cX1=int(M1['m10']/M1["m00"])
            cY1=int(M1["m01"]/M1["m00"])
            cv2.drawContours(img1,c1, -1, (0, 255, 0), 2)
            cv2.circle(img1, (cX1, cY1), 7, (255, 255, 255), -1)
            cv2.putText(img1, "center", (cX1 - 20, cY1 - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        else:
            cX1,cY1=0,0
        c2 = max(contours2, key = cv2.contourArea)
        M2=cv2.moments(c2)
        if M2["m00"] != 0:
            cX2=int(M2['m10']/M2["m00"])
            cY2=int(M2["m01"]/M2["m00"])
            cv2.drawContours(img2,c2, -1, (0, 255, 0), 2)
            cv2.circle(img2, (cX2, cY2), 7, (255, 255, 255), -1)
            cv2.putText(img2, "center", (cX2 - 20, cY2 - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        else:
            cX2,cY2=0,0
       
        # D2= dist.euclidean((cX2,cY2),(0,0))

        #Distance detection in pixels
        D=cX1+cX2
        #rough estimation in metres
        print(D/(2.54*100))
    else:
        print("0")

    #final calculations,based on cameras, with different foc_len
    # fin_dist=B*foc_len/(2*np.tan(0.94/2)*D)

    #show images      
    cv2.imshow("create",img1)
    cv2.imshow("create2",img2)
    if cv2.waitKey(10)==27:
        break
    count=count+1
