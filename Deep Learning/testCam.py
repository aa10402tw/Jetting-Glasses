import numpy as np
import cv2

import os
import glob
import copy

save_data = True
is_val = False
is_test = False


cap_1 = cv2.VideoCapture(1)


while(True):
    flag_1, cur_frame_1 = cap_1.read()

    cv2.imshow('frame', cur_frame_1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_1.release()
cv2.destroyAllWindows()
