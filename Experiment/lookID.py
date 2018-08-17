import os
import cv2
from cv2 import aruco


aruco_dict = aruco.custom_dictionary(20, 3, 1)
cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=aruco.DetectorParameters_create())
    frame = aruco.drawDetectedMarkers(frame, corners, ids, (255, 0, 255))
    cv2.imshow('Look IDs', frame)
    # 若按下 q 鍵則離開
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
