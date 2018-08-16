from jettingGlasses import *
from cameraParams import *

import pandas as pd
import glob
import os

camera = 'webcam'
name = 'test'

pos2marker = {'index_1': 5, 'index_2': 13, 'index_3': 1,
              'middle_1': 0, 'middle_2': 3, 'middle_3': 12,
              'ring_1': 6, 'ring_2': 7, 'ring_3': 8,
              'little_1': 0, 'little_2': 0, 'little_3': 0}

marker2pos = {v: k for k, v in pos2marker.items()}

cameraMatrix, distCoeffs = loda_camera_params(camera=camera)

JG = Jetting_Glasses(cameraMatrix, distCoeffs, need_acc=True)
draw = Draw3D()


def read_panticpant_data(name='', haptic=False):
    if name:
        subTitle = 'haptic' if haptic else 'no_haptic'
        file_name = 'data/csv/%s(%s).csv' % (name, subTitle)
        df = pd.read_csv(file_name, sep='\t')
        return df


df = read_panticpant_data(name=name, haptic=True)

for img_src, pos, pos_thick, time in zip(df['img_name'], df['pos'], df['pos_thick'], df['time']):
    frame = cv2.imread(img_src)
    JG.update_frame(frame)
    rayPoint, planeCenter, intersectPoint, dis = JG.ray_intersect(pos2marker[pos], pos_thick)
    frame = JG.get_frame(frame, corner=False, axis=False, tracker_corner=True, port=True, ray=True)
    frame_info = JG.get_frame_info()
    frame = cv2.resize(frame, get_resolution(camera))
    cv2.putText(frame, 'Pos : %s' % (pos), (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, 'Dis : %.4f' % (dis), (30, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, 'Time : %.4f' % (time), (30, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    if frame_info['error'] is not None:
        cv2.putText(frame, frame_info['error'], (30, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('frame', frame)

    c = cv2.waitKey(0)
    if c & 0xFF == ord('s'):
        draw.camera()
        draw.corner(frame_info)
        draw.port_ray(frame_info)
        draw.intersect(planeCenter, intersectPoint)
        draw.show()
        draw.__init__()
