import cv2
import cv2.aruco as aruco
import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from parameters import *

thickness = 0.02


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

    def track(self, points):
        ax = self.fig.gca(projection='3d')
        print(points)
        xs, ys, zs = [], [], []
        for p in points:
            xs.append(p[0])
            ys.append(p[1])
            zs.append(p[2])
        ax.scatter(xs, ys, zs, c='blue', marker='o')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim(np.array(xs).mean() - 0.05, np.array(xs).mean() + 0.05)
        ax.set_ylim(np.array(ys).mean() - 0.05, np.array(ys).mean() + 0.05)
        ax.set_zlim(np.array(zs).mean() - 0.05, np.array(zs).mean() + 0.05)

    def intersect(self, planeCenter, intersectPoint):
        ax = self.fig.gca(projection='3d')
        ax.scatter(intersectPoint[0], intersectPoint[1], intersectPoint[2], c='b', marker='x')  # hit
        ax.scatter(planeCenter[0], planeCenter[1], planeCenter[2], c='g', marker='x')  # center
        ax.plot([intersectPoint[0], planeCenter[0]], [intersectPoint[1], planeCenter[1]], [intersectPoint[2], planeCenter[2]], c='r')

    def line(self, _line):
        ax = self.fig.gca(projection='3d')
        xs, ys, zs = _line[0], _line[1], _line[2]
        ax.plot(xs, ys, zs, c='b')

    def plane(self, points, alpha=0.1):
        ax = self.fig.gca(projection='3d')
        x, y, z = points['x'], points['y'], points['z']
        data = np.c_[x, y, z]  # np.c_是按行连接两个矩阵，就是把两矩阵左右相加
        X, Y = np.meshgrid(x, y)
    # best-fit linear plane
        A = np.c_[data[:, 0], data[:, 1], np.ones(data.shape[0])]
        C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2])  # least-squares solution to equation Ax = b.
        Z = C[0] * X + C[1] * Y + C[2]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=alpha)

    def camera(self):
        ax = self.fig.gca(projection='3d')
        ax.scatter([0 for i in range(200)], [0 for i in range(200)], [i * 0.005 for i in range(200)], c=COLOR_CAMERA, marker='X')

    def port_ray(self, frame_info):
        tvec, rvec = frame_info['tvec_tracker'], frame_info['rvec_tracker']
        if(rvec is None):
            return
        r_mat, _ = cv2.Rodrigues(rvec)
        t_vec = tvec
        t_mat = np.array([t_vec, ] * 2).transpose()
        p_start, p_end = [tracker_offset_x, tracker_offset_y, 0], [tracker_offset_x, tracker_offset_y, 1]
        line = np.transpose(np.float32([[tracker_offset_x, tracker_offset_y, 0], [tracker_offset_x, tracker_offset_y, markerLength_tracker * 10]]))
        line_ = np.matmul(r_mat, line) + t_mat[0]
        ax = self.fig.gca(projection='3d')
        self.line(line_)
        # Draw port
        ax.scatter([line_[0][0]], [line_[1][0]], [line_[2][0]], c='blue', marker='o')

        t_mat = np.array([t_vec, ] * 4).transpose()
        corners = np.transpose(np.array([[tracker_offset_x + -1 * markerLength_tracker / 2, tracker_offset_y + markerLength_tracker / 2 * 7, 0],
                                         [tracker_offset_x + markerLength_tracker / 2, tracker_offset_y + markerLength_tracker / 2 * 7, 0],
                                         [tracker_offset_x + markerLength_tracker / 2, tracker_offset_y + -1 * markerLength_tracker / 2 * 7, 0],
                                         [tracker_offset_x + -1 * markerLength_tracker / 2, tracker_offset_y + -1 * markerLength_tracker / 2 * 7, 0]]))
        # Board Plane
        corners_ = np.matmul(r_mat, corners) + t_mat
        points = {'x': corners_[0][0], 'y': corners_[0][1], 'z': corners_[0][2]}
        self.plane(points, alpha=0.99)

    def tracker_corner(self, frame_info, draw_planes=True):
        ax = self.fig.gca(projection='3d')
        corners, markerLength, cameraMatrix, distCoeffs = frame_info['corners_tracker'], frame_info['markerLength'], frame_info['cameraMatrix'], frame_info['distCoeffs']
        rvecs, tvecs = frame_info['rvecs_tracker'], frame_info['tvecs_tracker']
        if(tvecs is None):
            return
        xs, ys, zs = [], [], []
        points = {'x': [], 'y': [], 'z': []}
        for i, t in enumerate(tvecs):
            r_mat, _ = cv2.Rodrigues(rvecs[i])
            t_mat = np.array([t[0], ] * 4).transpose()
            corners = np.transpose(np.array([[-1 * markerLength_tracker / 2, markerLength_tracker / 2, 0], [markerLength_tracker / 2, markerLength_tracker / 2, 0],
                                             [markerLength_tracker / 2, -1 * markerLength_tracker / 2, 0], [-1 * markerLength_tracker / 2, -1 * markerLength_tracker / 2, 0]]))
            corners_ = np.matmul(r_mat, corners) + t_mat

            xs += list(corners_[0])
            ys += list(corners_[1])
            zs += list(corners_[2])
            points = {'x': corners_[0], 'y': corners_[1], 'z': corners_[2]}
            if(draw_planes):
                self.plane(points)
            # self.plane(points_map, alpha=0.3)
        ax.scatter(xs, ys, zs, c=COLOR_TRACKER)
        ax.set_xlim(np.array(xs).mean() - 0.05, np.array(xs).mean() + 0.05)
        ax.set_ylim(np.array(ys).mean() - 0.05, np.array(ys).mean() + 0.05)
        ax.set_zlim(np.array(zs).mean() - 0.05, np.array(zs).mean() + 0.05)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

    def target_corner(self, frame_info, marker_id):
        ax = self.fig.gca(projection='3d')
        ids, rvecs, tvecs, markerLength = frame_info['ids'], frame_info['rvecs'], frame_info['tvecs'], frame_info['markerLength']

    def corner(self, frame_info, draw_planes=True):
        ax = self.fig.gca(projection='3d')
        ids, rvecs, tvecs, markerLength = frame_info['ids'], frame_info['rvecs'], frame_info['tvecs'], frame_info['markerLength']
        xs, ys, zs = [], [], []
        xs_m, ys_m, zs_m = [], [], []
        points = {'x': [], 'y': [], 'z': []}
        if(tvecs is None):
            return
        for i, t in enumerate(tvecs):
            r_mat, _ = cv2.Rodrigues(rvecs[i])
            t_mat = np.array([t[0], ] * 4).transpose()
            if ids[i] != tracker_id_left and ids[i] != tracker_id_right:
                corners = np.transpose(np.array([[-1 * markerLength / 2, markerLength / 2, 0], [markerLength / 2, markerLength / 2, 0],
                                                 [markerLength / 2, -1 * markerLength / 2, 0], [-1 * markerLength / 2, -1 * markerLength / 2, 0]]))
                corners_map = np.transpose(np.array([[-1 * markerLength / 2, markerLength / 2, -1 * thickness], [markerLength / 2, markerLength / 2, -1 * thickness],
                                                     [markerLength / 2, -1 * markerLength / 2, -1 * thickness], [-1 * markerLength / 2, -1 * markerLength / 2, -1 * thickness]]))
            else:
                corners = np.transpose(np.array([[-1 * markerLength_tracker / 2, markerLength_tracker / 2, 0], [markerLength_tracker / 2, markerLength_tracker / 2, 0],
                                                 [markerLength_tracker / 2, -1 * markerLength_tracker / 2, 0], [-1 * markerLength_tracker / 2, -1 * markerLength_tracker / 2, 0]]))

            corners_ = np.matmul(r_mat, corners) + t_mat
            xs += list(corners_[0])
            ys += list(corners_[1])
            zs += list(corners_[2])

            # corners_map = np.matmul(r_mat, corners_map) + t_mat
            # xs_m += list(corners_map[0])
            # ys_m += list(corners_map[1])
            # zs_m += list(corners_map[2])

            points = {'x': corners_[0], 'y': corners_[1], 'z': corners_[2]}
            # points_map = {'x': corners_map[0], 'y': corners_map[1], 'z': corners_map[2]}
            if(draw_planes):
                self.plane(points)
                # self.plane(points_map, alpha=0.3)
        ax.scatter(xs, ys, zs, c=COLOR_CORNER)
        # ax.scatter(xs_m, ys_m, zs_m, c=COLOR_CORNER)
        ax.set_xlim(np.array(xs).mean() - 0.05, np.array(xs).mean() + 0.05)
        ax.set_ylim(np.array(ys).mean() - 0.05, np.array(ys).mean() + 0.05)
        ax.set_zlim(np.array(zs).mean() - 0.05, np.array(zs).mean() + 0.05)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
