import cv2
import time

fitToEllipse = False
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(2)

fgbg = cv2.createBackgroundSubtractorMOG2()
j = 0

while(1):
    ret, frame = cap.read()
    
    #Convert each frame to gray scale and subtract the background
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)
        
        #Find contours
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
        
            # List to hold all areas
            areas = []

            for contour in contours:
                ar = cv2.contourArea(contour)
                areas.append(ar)
            
            max_area = max(areas, default = 0)

            max_area_index = areas.index(max_area)

            cnt = contours[max_area_index]

            M = cv2.moments(cnt)
            
            x, y, w, h = cv2.boundingRect(cnt)

            cv2.drawContours(fgmask, [cnt], 0, (255,255,255), 3, maxLevel = 0)
            
            if h < w:
                j += 1
                
            if j > 10:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                frame = cv2.copyMakeBorder(src=frame,
                        top= 10,
                        bottom= 10,
                        left= 10,
                        right= 10,
                        borderType=cv2.BORDER_CONSTANT,
                        dst=None,
                        value=[0, 0, 255])
            else:
                frame = cv2.copyMakeBorder(src=frame,
                        top= 10,
                        bottom= 10,
                        left= 10,
                        right= 10,
                        borderType=cv2.BORDER_CONSTANT,
                        dst=None,
                        value=[0, 255, 0])

            if h > w:
                j = 0 
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            
            cv2.namedWindow('video', flags=cv2.WINDOW_GUI_NORMAL)
            cv2.setWindowProperty('video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty('video', cv2.WND_PROP_TOPMOST, 1)
            cv2.resizeWindow('video', 775, 588)
            cv2.moveWindow('video', 522, 125)
            cv2.imshow('video', frame)
        
            if cv2.waitKey(33) == 27:
             break
    except Exception as e:
        break
cv2.destroyAllWindows()
