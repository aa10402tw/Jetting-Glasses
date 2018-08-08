import numpy as np
import cv2

import os
import glob
import copy

save_data = True
is_val = False
is_test = False

cap_1 = cv2.VideoCapture(1)
cap_2 = cv2.VideoCapture(2)
cap_3 = cv2.VideoCapture(3)
flag_1, cur_frame_1 = cap_1.read()
flag_2, cur_frame_2 = cap_2.read()
flag_3, cur_frame_3 = cap_3.read()

LABELS = [
    'index_1', 'index_2', 'index_3',
    'middle_1', 'middle_2', 'middle_3',
    'ring_1', 'ring_2', 'ring_3',
    'little_1', 'little_2', 'little_3',
    'palm', 'background'
]

label_index = 0
label = LABELS[label_index]
if is_test:
    label = 'test'
index = 0

num_frame_per_label = int(200)
num_frame_rest = int(100)

if save_data:
    for l in LABELS:
        if not os.path.isdir('./data/' + l):
            os.makedirs('./data/' + l)

if label == 'test':
    num_frame_per_label, num_frame_rest = 500, 100
    label_index = len(LABELS)
    is_val = False
    if not os.path.isdir('./test'):
        os.makedirs('./test')

file_list = glob.glob("./data/" + label + '/*')
if(len(file_list) != 0):
    for i, file in enumerate(file_list):
        if 'val_' in file:
            file_list[i] = file.split('val_')[-1]
    path = sorted(file_list, key=lambda x: int(os.path.split(x)[-1].split('.')[0]))[-1]
    index = int(os.path.split(path)[1].split('.')[0]) + 1
base_index = index

while(True):
    flag_1, cur_frame_1 = cap_1.read()
    flag_2, cur_frame_2 = cap_2.read()
    flag_3, cur_frame_3 = cap_3.read()
    frame = np.concatenate((cur_frame_1, cur_frame_2, cur_frame_3), axis=1)

    dot_frame = copy.copy(cur_frame_2)
    dot_frame[235:245, 315:325, :] = (255, 0, 0)
    display_frame = np.concatenate((cur_frame_1, dot_frame, cur_frame_3), axis=1)

    index += 1
    if((index - base_index) % (num_frame_per_label + num_frame_rest) > num_frame_rest):
        if(is_val):
            file_name = "./data/" + label + '/val_' + str(index) + ".jpg"
        else:
            file_name = "./data/" + label + '/' + str(index) + ".jpg"
        if save_data:
            cv2.imwrite(file_name, frame)
        cv2.putText(display_frame, str(label), (50, 50), 0, 1, (255, 0, 0), 3)
        if((index - base_index) % (num_frame_per_label + num_frame_rest) > num_frame_per_label):
            cv2.putText(display_frame, str(label), (50, 50), 0, 1, (0, 0, 255), 3)
    else:
        cv2.putText(display_frame, str(label), (50, 50), 0, 1, (255, 255, 255), 3)

    # Display the resulting frame

    cv2.imshow('frame', display_frame)

    if((index - base_index) % (num_frame_per_label + num_frame_rest) == 0):
        label_index += 1
        if(label_index >= len(LABELS)):
            break
        label = LABELS[label_index]

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_1.release()
cap_2.release()
cv2.destroyAllWindows()
