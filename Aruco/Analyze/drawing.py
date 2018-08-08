import cv2
import cv2.aruco as aruco
import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from parameters import *


class Draw3D():
    def __init__(self):
        self.fig = plt.figure()

    def adjust_lim(self, start, end):
        ax = self.fig.gca(projection='3d')
        ax.set_xlim(min(start[0], end[0]) - 0.05, max(start[0], end[0]) + 0.05)
        ax.set_ylim(min(start[1], end[1]) - 0.05, max(start[1], end[1]) + 0.05)
        ax.set_zlim(min(start[2], end[2]) - 0.05, max(start[2], end[2]) + 0.05)

    def show(self):

        plt.show()

    def intersect(self, planeCenter, intersectPoint):
        ax = self.fig.gca(projection='3d')
        ax.scatter(intersectPoint[0], intersectPoint[1], intersectPoint[2], c='b', marker='x')  # hit
        ax.scatter(planeCenter[0], planeCenter[1], planeCenter[2], c='g', marker='x')  # center
        ax.plot([intersectPoint[0], planeCenter[0]], [intersectPoint[1], planeCenter[1]], [intersectPoint[2], planeCenter[2]], c='r')

    def line(self, _line):
        ax = self.fig.gca(projection='3d')
        xs, ys, zs = _line[0], _line[1], _line[2]
        ax.plot(xs, ys, zs, c='b')

    def plane(self, points):
        ax = self.fig.gca(projection='3d')
        x, y, z = points['x'], points['y'], points['z']
        data = np.c_[x, y, z]  # np.c_是按行连接两个矩阵，就是把两矩阵左右相加
        X, Y = np.meshgrid(x, y)
    # best-fit linear plane
        A = np.c_[data[:, 0], data[:, 1], np.ones(data.shape[0])]
        C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2])  # least-squares solution to equation Ax = b.
        Z = C[0] * X + C[1] * Y + C[2]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.1)

    def camera(self):
        ax = self.fig.gca(projection='3d')
        ax.scatter([0 for i in range(200)], [0 for i in range(200)], [i * 0.005 for i in range(200)], c=COLOR_CAMERA, marker='X')

    def port_ray(self, frame_info):
        def get_line(tracker_id, offset):
            if tracker_id not in ids:
                return False, None
            idx = list(ids).index(tracker_id)
            r_mat, _ = cv2.Rodrigues(rvecs[idx])
            t_vec = tvecs[idx]
            t_mat = np.array([t_vec[0], ] * 2).transpose()
            # move offset
            p_start, p_end = [0, -1 * markerLength * offset, 0], [0, -1 * markerLength * offset, 1]
            line = np.transpose(np.array([p_start, p_end]))
            line_ = np.matmul(r_mat, line) + t_mat
            return True, line_

        ax = self.fig.gca(projection='3d')
        ids, tracker_id_left, tracker_id_right = frame_info['ids'], frame_info['tracker_id_left'], frame_info['tracker_id_right']
        offset_left, offset_right = frame_info['offset_left'], frame_info['offset_right']
        rvecs, tvecs = frame_info['rvecs'], frame_info['tvecs']

        # t_mat = np.array([t_vec[0],]*4).transpose()
        # corners = np.transpose( np.array( [[-1*markerLength/2,markerLength/2,0], [markerLength/2,markerLength/2,0],
        # 		[markerLength/2,-1*markerLength/2,0], [-1*markerLength/2,-1*markerLength/2,0]] ) )
        # corners_ = np.matmul(r_mat, corners) + t_mat
        # points = {'x':corners_[0], 'y':corners_[1], 'z':corners_[2]}
        # self.plane(points)
        # Line
        flag_l, line_l = get_line(tracker_id_left, offset_left)
        flag_r, line_r = get_line(tracker_id_right, offset_right)
        line, cnt = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]), 0
        if(flag_l):
            cnt += 1
            line += line_l
        if(flag_r):
            cnt += 1
            line += line_r
        if(cnt == 0):
            return
        else:
            line = line / cnt
            self.line(line)
            # Draw port
            ax.scatter([line[0][0]], [line[1][0]], [line[2][0]], c='blue', marker='o')

    def corner(self, frame_info, draw_planes=True):
        ax = self.fig.gca(projection='3d')
        rvecs, tvecs, markerLength = frame_info['rvecs'], frame_info['tvecs'], frame_info['markerLength']
        xs, ys, zs = [], [], []
        points = {'x': [], 'y': [], 'z': []}
        for i, t in enumerate(tvecs):
            r_mat, _ = cv2.Rodrigues(rvecs[i])
            t_mat = np.array([t[0], ] * 4).transpose()
            corners = np.transpose(np.array([[-1 * markerLength / 2, markerLength / 2, 0], [markerLength / 2, markerLength / 2, 0],
                                             [markerLength / 2, -1 * markerLength / 2, 0], [-1 * markerLength / 2, -1 * markerLength / 2, 0]]))
            corners_ = np.matmul(r_mat, corners) + t_mat
            xs += list(corners_[0])
            ys += list(corners_[1])
            zs += list(corners_[2])
            points = {'x': corners_[0], 'y': corners_[1], 'z': corners_[2]}
            if(draw_planes):
                self.plane(points)
        ax.scatter(xs, ys, zs, c=COLOR_CORNER)
        ax.set_xlim(np.array(xs).mean() - 0.05, np.array(xs).mean() + 0.05)
        ax.set_ylim(np.array(ys).mean() - 0.05, np.array(ys).mean() + 0.05)
        ax.set_zlim(np.array(zs).mean() - 0.05, np.array(zs).mean() + 0.05)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
