import  cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

#############
wCam, hCam = 648,448
frameR= 100 #frame reduction
#smoothening=20
#############
pTime = 0
plocX,plocY = 0,0
clocX,clocY = 0,0
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4,480)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
print(wScr,hScr)
while(True):
    # 1 Find Hand Tracking Module
    success , img=cap.read()
    img=detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)
    
    
    # 2 Get the Tip of the Index and the Middle Finger
    if len(lmlist)!=0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        print(x1,y1,x2,y2)
        # 3 Check Which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        # 4 Only Index Finger :Moving Mode
        if fingers[1]== 1 and fingers[2]==0:

            # 5 Convert coordinates
            
            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            # 6 Smoothening the Values
            #clocX=plocX +(x3-plocX)/smoothening
            #clocY=plocY +(x3-plocY)/smoothening
            # 7 Move Mouse
            autopy.mouse.move(wScr-x3,y3)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            #plocX,plocY=clocX,clocY
        # 8 Both Index and Middle finger are up : Clicking Mode
        if fingers[1]== 1 and fingers[2]==1:
            # 9 Find Distance Between Fingers
            length,img, lineinfo = detector.findDistance(8,12,img)
            print(length)
            # 10 Click Mouse if Distance is Short
            if length<48:
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()

        
        
        # 11 Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    # 12 Display
    cv2.imshow("videoss",img)
    cv2.waitKey(1)