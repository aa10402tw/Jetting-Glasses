from jettingGlasses import *
from cameraParams import *

import pandas as pd
import glob
import os

camera = 'webcam'

pos2marker = {'index_1': 1, 'index_2': 3, 'index_3': 5,
              'middle_1': 12, 'middle_2': 13, 'middle_3': 14,
              'ring_1': 16, 'ring_2': 17, 'ring_3': 19}

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


def analyze_data(df):
    pos_list = []
    dis_list = []
    time_list = []
    for img_src, pos, pos_thick, time in zip(df['img_name'], df['pos'], df['pos_thick'], df['time']):
        frame = cv2.imread(img_src)
        JG.update_frame(frame)
        rayPoint, planeCenter, intersectPoint, dis = JG.ray_intersect(pos2marker[pos], pos_thick)
        pos_list.append(pos)
        dis_list.append(dis)
        time_list.append(time)
    return pos_list, dis_list, time_list


df_names = pd.read_csv('./data/csv/all_panticpant.csv', sep='\t')
names = list(df_names['name'].values)
avg_dis_h, avg_dis_nh, avg_time_h, avg_time_nh = [], [], [], []
for name in names:
    df_h = read_panticpant_data(name=name, haptic=True)
    df_nh = read_panticpant_data(name=name, haptic=False)
    pos_list_h, dis_list_h, time_list_h = analyze_data(df_h)
    pos_list_nh, dis_list_nh, time_list_nh = analyze_data(df_nh)
    pos = ['index_1', 'index_2', 'index_3', 'middle_1', 'middle_2', 'middle_3', 'ring_1', 'ring_2', 'ring_3']
    dis_h = [dis_list_h[pos_list_h.index(pos[i])] for i in range(len(pos))]
    time_h = [time_list_h[pos_list_h.index(pos[i])] for i in range(len(pos))]
    dis_nh = [dis_list_nh[pos_list_nh.index(pos[i])] for i in range(len(pos))]
    time_nh = [time_list_nh[pos_list_nh.index(pos[i])] for i in range(len(pos))]

    avg_dis_h.append(np.nanmean(dis_h) if not np.isnan(np.nanmean(dis_h)) else 'Nan')
    avg_dis_nh.append(np.nanmean(dis_nh) if not np.isnan(np.nanmean(dis_nh)) else 'Nan')
    avg_time_h.append(np.nanmean(time_h))
    avg_time_nh.append(np.nanmean(time_nh))

    dis_h = ['NaN' if np.isnan(x) else x for x in dis_h]
    dis_nh = ['NaN' if np.isnan(x) else x for x in dis_nh]

    df = pd.DataFrame({'Pos': pos, 'Dis_hap': dis_h, 'Time_hap': time_h, 'Dis_nHap': dis_nh, 'Time_nHap': time_nh})
    df = df[['Pos', 'Dis_hap', 'Time_hap', 'Dis_nHap', 'Time_nHap']]
    writer = pd.ExcelWriter('./AnalyzeResult/%s.xlsx' % (name))
    df.to_excel(writer, index=False)
    writer.save()


df = pd.DataFrame({'Name': names, 'Avg_Dis_hap': avg_dis_h, 'Avg_Time_hap': avg_time_h, 'Avg_Dis_nHap': avg_dis_nh, 'Avg_Time_nHap': avg_time_nh})
df = df[['Name', 'Avg_Dis_hap', 'Avg_Time_hap', 'Avg_Dis_nHap', 'Avg_Time_nHap']]
writer = pd.ExcelWriter('./AnalyzeResult/summary.xlsx')
df.to_excel(writer, index=False)
writer.save()
