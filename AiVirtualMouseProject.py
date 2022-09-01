import cv2
import numpy as np
# from mediapipe import HandTrackingModule as htm
import HandTrackingModule as htm
import time
import autopy
import pyautogui
# pyautogui.PAUSE = 1 # 代表每次呼叫執行動作之後都會停一秒
# pyautogui.FAILSAFE = True # 啟用失效安全防護
# 
wCam , hCam = 640, 480
frameR = 100 # Frame Reduction
wScr, hScr = autopy.screen.size()  # 自己螢幕尺寸
# wScr, hScr = pyautogui.size()
smoothening = 7

"""
cap = cv2.VideoCapture(-1) on linux
cap = cv2.VideoCapture(0) on windows

"""
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)
pTime=0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
# clocX, clocY = pyautogui.position() #獲取當前滑鼠的位置
detector = htm.handDetector(maxHands=1)

"""
[
    [0, 233, 461], 
    [1, 255, 457], 
    [2, 270, 455], 
    [3, 282, 451], 
    [4, 287, 448], 
    [5, 256, 449], 
    [6, 272, 435], 
    [7, 277, 433], 
    [8, 278, 433], 
    [9, 249, 445], 
    [10, 268, 428], 
    [11, 274, 429], 
    [12, 273, 431], 
    [13, 246, 442], 
    [14, 264, 428], 
    [15, 270, 430], 
    [16, 270, 433], 
    [17, 243, 440], 
    [18, 256, 430], 
    [19, 260, 429], 
    [20, 262, 431]
]

"""
while True:
    # TODO 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # print("===> ",lmList)
    # print("========================")
    clocX, clocY = pyautogui.position() #獲取當前滑鼠的位置
    # TODO 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1,y1 = lmList[8][1:] # index finger
        x2,y2 = lmList[12][1:] # middle finger
        
        # print(x1,y1,x2,y2)
        
        # TODO 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(
            img, 
            (frameR, frameR), 
            (wCam - frameR, hCam - frameR),
            (255, 0, 255), 
            2
        )

        # TODO 4. Only Index Finger : Moving Mode
        if fingers[1]==1 and fingers[2]==0:

            # TODO 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            
            # TODO 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            
            # TODO 7. Move Mouse
            autopy.mouse.move(wScr-clocX,clocY)  # wScr-x3: 解決滑鼠左右移動相反的問題
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # TODO 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1]==1 and fingers[2]==1:

            # ----------------------------
            # TODO 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            
            # TODO 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # ----------------------------

         
            # TODO 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8,12,img)
            # print(length)  # 食指與中指距離
              
                
            # TODO 10. Click mouse if distance short
            if length<40:
                """"""
                
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click() # click'left') 
                # autopy.mouse.move(wScr-clocX,clocY)
                

                # pyautogui.dragRel(wScr-clocX,clocY, 2, button='left')
                # autopy.mouse.smooth_move(clocX-plocX, clocY-plocY)
                # autopy.mouse.toggle(button=autopy.mouse.Button.LEFT, down=False)
                plocX, plocY = clocX, clocY
         
         
        if fingers[1]==1 and fingers[0]==1:
            # ----------------------------
            # TODO 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            
            # TODO 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # ----------------------------
            pyautogui.dragRel(-100, 0,  button='left')  
        if fingers[1]==1 and fingers[4]==1:
            # ----------------------------
            # TODO 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            
            # TODO 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # ----------------------------
            pyautogui.dragRel(100, 0,  button='left')  
        

    #  TODO 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(
        img, 
        str(int(fps)), 
        (20, 50), 
        cv2.FONT_HERSHEY_PLAIN,
        3,
        (255, 0, 0), 
        3
        )
    #  TODO 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)