import numpy as np
import cv2
import os
import glob
import copy

CAMERA_LEFT = 1
CAMERA_MID = 2
CAMERA_RIGHT = 3

if __name__ == '__main__':
    cap_L = cv2.VideoCapture(CAMERA_LEFT)
    cap_M = cv2.VideoCapture(CAMERA_MID)
    cap_R = cv2.VideoCapture(CAMERA_RIGHT)
    flag_L, frame_L = cap_L.read()
    flag_M, frame_M = cap_M.read()
    flag_R, frame_R = cap_R.read()
    if (flag_L and flag_M and flag_R):
        while(True):
            flag_L, frame_L = cap_L.read()
            flag_M, frame_M = cap_M.read()
            flag_R, frame_R = cap_R.read()
            frame = np.concatenate((frame_L, frame_M, frame_R), axis=1)
            frame = cv2.resize(frame, (300, 300))
            cv2.putText(frame, "Left", (50, 150), 0, 1, (255, 0, 0), 3)
            cv2.putText(frame, "Mid", (150, 150), 0, 1, (255, 0, 0), 3)
            cv2.putText(frame, "Right", (250, 150), 0, 1, (255, 0, 0), 3)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap_1.release()
        cv2.destroyAllWindows()
    else:
        print('Left Camera:%r, Mid Camera:%r, Right Camera:%r' % (flag_L, flag_M, flag_R))
