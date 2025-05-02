import cv2
import mediapipe as mp
import time
import pose_estimation_module as pem
import numpy as np


cap = cv2.VideoCapture("ai_trainer/1.mp4")  
# cap = cv2.VideoCapture(0)  

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

time.sleep(2)  # Give the camera time to initialize

p_time = 0
c_time = 0



detector = pem.pose_detector()

count = 0
dir  = 0


while True:
    success, img = cap.read()

    if not success or img is None:
        print("Error: Failed to capture image")  
        break  # Exit if no frame is captured
    
    # img = cv2.imread("ai_trainer/test.jpg")           ## reading a image for testing 
    
    img = cv2.resize(img, (720, 720))
    
    img = detector.find_pose(img, False)
    lm_list = detector.find_position(img, False)
    # print(lm_list)
    
    if len(lm_list) != 0:
        ## right arm
        # angle = detector.find_angle(img, 12, 14, 16)
        ## left arm
        angle = detector.find_angle(img, 11, 13, 15)
        per = np.interp(angle, (80, 180), (0, 100))
        bar = np.interp(angle, (80, 180), (650, 100))       ## setting up value for the bar 
        # print(angle, per)
        
        #3 check for dumpbell curls
        # color = (255, 0, 255)                  ## this is for the bar color 
        if per == 100:
            # color = (0, 255, 0)                ## this is useful when we work with the draw bar
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            # color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)
        
        ## draw bar
        # cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)                        ##### we have to fix it as per the webcam  size, so fix it carefully
        # cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        # cv2.putText(img, f'{int(per)}', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)
        
        
        ## draw curl count
        cv2.rectangle(img, (0, 500), (150, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (5, 670), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 0), 2)
    
        
    
    
    c_time  = time.time()
    fps = 1/(c_time - p_time)
    p_time = c_time
    
    cv2.putText(img, f'FPS: {str(int(fps))}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 3)



    cv2.imshow("Image", img)   # display the proccessed fame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Press 'q' to exit