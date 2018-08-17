import warnings
warnings.filterwarnings("ignore")

import tkinter as tk
import pandas as pd
import numpy as np
import cv2
import os
import glob
import copy

from testCamera import *


USER_NAME = ''
MODE = 1

save_data = False

LABELS = [
    'index_1', 'index_2', 'index_3',
    'middle_1', 'middle_2', 'middle_3',
    'ring_1', 'ring_2', 'ring_3',
    'little_1', 'little_2', 'little_3',
    'palm', 'background'
]

CIRCLE_POS = [(376, 95), (364, 171), (346, 270),
              (241, 62), (245, 148), (247, 260),
              (149, 90), (154, 172), (166, 280),
              (38, 210), (63, 263), (87, 327),
              (230, 470), (-1, -1)]

num_frame_per_label = int(200)
num_frame_rest = int(100)


def startCollectData(app):
    global MODE
    app.quit()
    app.destroy()

    hand_img = cv2.imread('right_hand.jpg')
    background_img = cv2.imread('background.jpg')
    cv2.namedWindow('Hand')        # Create a named window
    cv2.moveWindow('Hand', 500, 20)  # Move it to (40,30)
    cap_L = cv2.VideoCapture(CAMERA_LEFT)
    cap_M = cv2.VideoCapture(CAMERA_MID)
    cap_R = cv2.VideoCapture(CAMERA_RIGHT)

    base_path = './data/%s/mode%s/' % (USER_NAME, MODE)

    if(save_data):
        for label in LABELS:
            if not os.path.isdir(base_path + label):
                os.makedirs(base_path + label)
    label_idx = 0
    frame_count = 0
    while True:
        flag_L, frame_L = cap_L.read()
        flag_M, frame_M = cap_M.read()
        flag_R, frame_R = cap_R.read()
        frame_count += 1
        label = LABELS[label_idx]
        if(label == 'background'):
            display_frame = copy.copy(background_img)
        else:
            display_frame = copy.copy(hand_img)

        if(frame_count <= num_frame_rest):
            cv2.circle(display_frame, CIRCLE_POS[label_idx], 5, (255, 100, 100), -1)
            cv2.putText(display_frame, "Preparing", (50, 50), 0, 1, (255, 100, 100), 3)
        elif(frame_count <= num_frame_per_label + num_frame_rest):
            cv2.circle(display_frame, CIRCLE_POS[label_idx], 5, (255, 0, 0), -1)
            cv2.putText(display_frame, "Recording", (50, 50), 0, 1, (255, 0, 0), 3)
            # frame = np.concatenate((frame_L, frame_M, frame_R), axis=1)
            # frame = cv2.resize(frame, (300, 300))
            if save_data:
                img_name = os.path.join(base_path, label, '%i.jpg' % (frame_count - num_frame_rest))
                print(img_name)
                # cv2.imwrite(img_name, frame)

        else:
            label_idx += 1
            frame_count = 0
        cv2.imshow('Hand', cv2.resize(display_frame, (500, 700)))
        c = cv2.waitKey(1)
        if c & 0xFF == ord('q') or label_idx >= len(LABELS):
            break

    cv2.destroyAllWindows()

    cap_L.release()
    cap_M.release()
    cap_R.release()

    if MODE < 3:
        MODE += 1
        app = DataApp()
        app.title("Collect Data")
        app.mainloop()


class DataApp(tk.Tk):

    def __init__(self, mode=0):
        tk.Tk.__init__(self)
        global MODE
        global USER_NAME
        self.geometry("%ix%i" % (800, 500))
        self.frame = tk.Frame(width=800, height=500, colormap="new")
        self.frame.place(relx=.5, rely=.5, anchor='c')
        self.frame_info = tk.Label(self.frame, text='請輸入姓名(英文)', font=("Monospace", 20))
        self.textBox_user_name = tk.Text(self.frame, height=1, width=20, font=("Monospace", 20))
        self.textBox_user_name.insert(tk.END, USER_NAME)
        self.buttonCommit_Mode1 = tk.Button(self.frame, height=1, width=10, text="Mode1", font=("Monospace", 20),
                                            command=lambda: self.commit_name_mode(mode=1))
        self.buttonCommit_Mode2 = tk.Button(self.frame, height=1, width=10, text="Mode2", font=("Monospace", 20),
                                            command=lambda: self.commit_name_mode(mode=2))
        self.buttonCommit_Mode3 = tk.Button(self.frame, height=1, width=10, text="Mode3", font=("Monospace", 20),
                                            command=lambda: self.commit_name_mode(mode=3))
        self.frame_info.place(relx=.5, rely=.4, anchor='c')
        self.textBox_user_name.place(relx=.5, rely=.5, anchor='c')
        if(MODE == 1):
            self.buttonCommit_Mode1.place(relx=.3, rely=.6, anchor='c')
        elif(MODE == 2):
            self.buttonCommit_Mode2.place(relx=.5, rely=.6, anchor='c')
        elif (MODE == 3):
            self.buttonCommit_Mode3.place(relx=.7, rely=.6, anchor='c')

    def commit_name_mode(self, mode=0):
        global MODE
        global USER_NAME
        USER_NAME = self.textBox_user_name.get("1.0", "end-1c")
        if(USER_NAME.strip()):
            if not os.path.isfile('./data/names.csv'):
                df = pd.DataFrame({'name': [USER_NAME]})
                df.to_csv('./data/names.csv', sep='\t', index=False)
            else:
                df_names = pd.read_csv('./data/names.csv', sep='\t')
                names = list(df_names['name'].values)
                if USER_NAME not in names:
                    names.append(USER_NAME)
                    df_names = pd.DataFrame({'name': names})
                    df_names.to_csv('./data/names.csv', sep='\t', index=False)

            startCollectData(self)
        else:
            print('user_name can not be empty')


if __name__ == '__main__':
    app = DataApp(MODE)
    app.title("Collect Data")
    app.mainloop()
