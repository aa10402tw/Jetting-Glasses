import cv2
import cv2.aruco as aruco
import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import copy

from drawing import *
from parameters import *


class Jetting_Glasses:

    def __init__(self, cameraMatrix, distCoeffs):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters_create()
        self.markerLength = markerLength
        self.cameraMatrix = cameraMatrix
        self.distCoeffs = distCoeffs
        self.offset_left = offset_left
        self.offset_right = offset_right
        self.tracker_id_left = tracker_id_left
        self.tracker_id_right = tracker_id_right
        self.NULL_POINT = NULL_POINT

    def update_frame(self, frame):
        self.frame = frame
        self.corners, self.ids, self.rejectedImgPoints = aruco.detectMarkers(self.frame, self.aruco_dict, parameters=self.parameters)
        self.rvecs, self.tvecs, self._corners = aruco.estimatePoseSingleMarkers(self.corners, self.markerLength, self.cameraMatrix, self.distCoeffs)

    def get_frame(self, frame, corner=False, axis=False, port=False, ray=False):
        frame = self.frame if frame is None else frame
        frame_ = copy.copy(frame)
        if(self.ids is None):
            return frame_
        if(corner):
            frame_ = self.get_frame_with_corner(frame_)
        if(axis):
            frame_ = self.get_frame_with_axis(frame_)
        if(port):
            frame_ = self.get_frame_with_port(frame_)
        if(ray):
            frame_ = self.get_frame_with_ray(frame_)
        return frame_

    def get_frame_with_corner(self, frame=None):
        frame = self.frame if frame is None else frame
        frame_ = copy.copy(frame)
        if(self.ids is None):
            return frame_
        frame_with_corner = aruco.drawDetectedMarkers(frame_, self.corners, self.ids, (255, 0, 0))
        return frame_with_corner

    def get_frame_with_axis(self, frame=None):
        frame = self.frame if frame is None else frame
        frame_ = copy.copy(frame)
        if(self.ids is None):
            return frame_
        for i in range(len(self.ids)):
            frame_with_axis = cv2.aruco.drawAxis(frame_, self.cameraMatrix, self.distCoeffs, self.rvecs[i], self.tvecs[i], self.markerLength * 2)
        return frame_with_axis

    def get_frame_with_port(self, frame=None):
        frame = self.frame if frame is None else frame
        return self.get_frame_with_ray(frame, only_port=True)

    def get_frame_with_ray(self, frame=None, only_port=False):
        def get_imgPoints(tracker_id, offset):
            if(self.ids is None):
                return False, None
            if tracker_id not in self.ids:
                return False, None
            idx = list(self.ids).index(tracker_id)
            imagePoints, jacobian = cv2.projectPoints(np.float32([[0, -1 * markerLength * offset, 0], [0, -1 * markerLength * offset, 0.1]]), self.rvecs[idx], self.tvecs[idx], self.cameraMatrix, self.distCoeffs)
            return True, imagePoints
        frame = self.frame if frame is None else frame
        frame_ = copy.copy(frame)
        flag_l, imgPoints_l = get_imgPoints(self.tracker_id_left, offset_left)
        flag_r, imgPoints_r = get_imgPoints(self.tracker_id_right, offset_right)
        imagePoints, cnt = np.array([[[0.0, 0.0]], [[0.0, 0.0]]]), 0
        if flag_l:
            imagePoints += imgPoints_l
            cnt += 1
        if flag_r:
            imagePoints += imgPoints_r
            cnt += 1
        if cnt != 0:
            imagePoints = (imagePoints / cnt).astype('int32')
            if only_port:
                frame_with_ray = cv2.line(frame_, tuple(imagePoints[0][0]), tuple(imagePoints[0][0]), (255, 0, 0), 8)
            else:
                frame_with_ray = cv2.line(frame_, tuple(imagePoints[0][0]), tuple(imagePoints[1][0]), (255, 0, 0), 3)
            return frame_with_ray
        return frame

    def get_plane(self, marker_id=-1):
        if(self.ids is None):
            return self.NULL_POINT, None
        if marker_id not in self.ids:
            return self.NULL_POINT, None
        idx = list(self.ids).index(marker_id)
        r_mat, _ = cv2.Rodrigues(self.rvecs[idx])
        t_vec = self.tvecs[idx]
        t_mat = np.array([t_vec[0], ] * 2).transpose()
        p_origin, p_norm = [0, 0, 0], [0, 0, 1]
        line = np.transpose(np.array([p_origin, p_norm]))
        line_ = np.matmul(r_mat, line) + t_mat
        line_ = np.transpose(line_)
        planePoint = line_[0]
        planeNormal = (line_[1] - line_[0]) / np.linalg.norm(line_[1] - line_[0])
        return planePoint, planeNormal

    def get_ray_half(self, tracker_id, offset):
        if tracker_id not in self.ids:
            return False, None, None
        idx = list(self.ids).index(tracker_id)
        r_mat, _ = cv2.Rodrigues(self.rvecs[idx])
        t_vec = self.tvecs[idx]
        t_mat = np.array([t_vec[0], ] * 2).transpose()
        p_origin, p_norm = [0, -1 * markerLength * offset, 0], [0, -1 * markerLength * offset, 1] 		# move offset
        line = np.transpose(np.array([p_origin, p_norm]))
        line_ = np.matmul(r_mat, line) + t_mat
        line_ = np.transpose(line_)
        rayPoint = line_[0]
        rayDirection = (line_[1] - line_[0]) / np.linalg.norm(line_[1] - line_[0])
        return True, rayPoint, rayDirection

    def get_ray(self):
        rayPoint, rayDirection = np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0])
        flag_l, rayPoint_l, rayDirection_l = self.get_ray_half(self.tracker_id_left, self.offset_left)
        flag_r, rayPoint_r, rayDirection_r = self.get_ray_half(self.tracker_id_right, self.offset_right)
        cnt = 0.0
        if flag_l:
            rayPoint += rayPoint_l
            rayDirection += rayDirection_l
            cnt += 1.0
        if flag_r:
            rayPoint += rayPoint_r
            rayDirection += rayDirection_r
            cnt += 1.0

        if cnt == 0:
            print('Error: Can not locate injection port !')
            return NULL_POINT, NULL_POINT
        else:
            return rayPoint / cnt, rayDirection / cnt

    def LinePlaneCollision(self, planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6):
        ndotu = planeNormal.dot(rayDirection)
        if abs(ndotu) < epsilon:
            raise RuntimeError("no intersection or line is within plane")
        w = rayPoint - planePoint
        si = -planeNormal.dot(w) / ndotu
        Psi = w + si * rayDirection + planePoint
        return Psi

    def distance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)

    def ray_intersect(self, marker_id):
        planeCenter, planeNormal = self.get_plane(marker_id)
        rayPoint, rayDirection = self.get_ray()
        if(np.any(np.isnan(planeCenter)) or np.any(np.isnan(rayPoint))):
            return self.NULL_POINT, self.NULL_POINT, self.NULL_POINT, np.nan,
        intersectPoint = self.LinePlaneCollision(planeNormal, planeCenter, rayDirection, rayPoint)
        dis = self.distance(planeCenter, intersectPoint)
        print('Plane Center:%s \nRay Intersect:%s \nDistance:[%s (m)]' % (planeCenter, intersectPoint, dis))
        return (rayPoint, planeCenter, intersectPoint, dis)

    def get_frame_info(self):
        return {'corners': self.corners, 'ids': self.ids, 'rvecs': self.rvecs,
                'tvecs': self.tvecs, 'markerLength': self.markerLength,
                'tracker_id_left': self.tracker_id_left, 'tracker_id_right': self.tracker_id_right,
                'offset_left': self.offset_left, 'offset_right': self.offset_right}
