import cv2
import cv2.aruco as aruco
import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import copy

from board import *
from drawing import *
from parameters import *


class Jetting_Glasses:

    def __init__(self, cameraMatrix, distCoeffs, need_acc=False):
        self.arucoTrackerBoard = ArucoBoard(nMarkers=10, markerSize=3, markerLength=0.012, markerSeparation=0.0012, randomSeed=10, size=(1, 10))
        self.arucoTrackerBoard = ArucoBoard(nMarkers=9, markerSize=3, markerLength=0.012, markerSeparation=0.0012, randomSeed=10, size=(3, 3))
        self.arucoMarkerBoard = ArucoBoard(nMarkers=20, markerSize=3, markerLength=0.012, markerSeparation=0.003, randomSeed=1, size=(2, 10))
        self.aruco_dict = self.arucoMarkerBoard.getDict()
        self.tracker_dict = self.arucoTrackerBoard.getDict()
        self.parameters = aruco.DetectorParameters_create()
        if need_acc:
            self.parameters.errorCorrectionRate = 0.4
            self.parameters.minCornerDistanceRate = 0.01
            self.parameters.minMarkerDistanceRate = 0.01
            self.parameters.cornerRefinementMethod = aruco.CORNER_REFINE_APRILTAG
            self.parameters.cornerRefinementMaxIterations = 100
            self.parameters.cornerRefinementMinAccuracy = 0.01
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
        self.error = ''
        self.corners, self.ids, self.rejectedImgPoints = aruco.detectMarkers(self.frame, self.aruco_dict, parameters=self.parameters)
        self.rvecs, self.tvecs, self._corners = aruco.estimatePoseSingleMarkers(self.corners, self.markerLength, self.cameraMatrix, self.distCoeffs)

        self.corners_tracker, self.ids_tracker, _ = aruco.detectMarkers(self.frame, self.tracker_dict, parameters=self.parameters)
        self.rvecs_tracker, self.tvecs_tracker, _ = aruco.estimatePoseSingleMarkers(self.corners_tracker, markerLength_tracker, self.cameraMatrix, self.distCoeffs)
        size = self.arucoTrackerBoard.getBoardSize()
        board = aruco.GridBoard_create(size[0], size[1], markerLength_tracker, markerSeparation_tracker, self.tracker_dict)

        _, self.rvec_tracker, self.tvec_tracker = aruco.estimatePoseBoard(self.corners_tracker, self.ids_tracker, board, self.cameraMatrix, self.distCoeffs)

    def get_frame(self, frame, corner=False, axis=False, port=False, ray=False, tracker_corner=False):
        frame = self.frame if frame is None else frame
        frame_ = copy.copy(frame)
        if(self.ids is not None):
            if(corner):
                frame_ = self.get_frame_with_corner(frame_)
            if(axis):
                frame_ = self.get_frame_with_axis(frame_)
        if(self.ids_tracker is not None):
            if(tracker_corner):
                frame_ = self.get_frame_with_tracker_corner(frame_)
            if(port):
                frame_ = self.get_frame_with_port(frame_)
            if(ray):
                frame_ = self.get_frame_with_ray(frame_)

        return frame_

    def get_frame_with_tracker_corner(self, frame):
        frame = self.frame if frame is None else frame
        frame_ = copy.copy(frame)
        if(self.ids_tracker is None):
            return frame_
        frame_ = aruco.drawDetectedMarkers(frame_, self.corners_tracker, self.ids_tracker, (0, 0, 255))
        return frame_

    def get_frame_with_board(self, frame=None):
        frame = self.frame if frame is None else frame
        frame_ = copy.copy(frame)
        if(self.ids_tracker is None):
            return frame_
        # frame_ = aruco.drawDetectedMarkers(frame_, self.corners_tracker, self.ids_tracker, (0, 0, 255))
        frame_with_axis = cv2.aruco.drawAxis(frame_, self.cameraMatrix, self.distCoeffs, self.rvec_tracker, self.tvec_tracker, markerLength_tracker * 1)
        return frame_with_axis

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
            frame_with_axis = cv2.aruco.drawAxis(frame_, self.cameraMatrix, self.distCoeffs, self.rvecs[i], self.tvecs[i], self.markerLength * 1)
        return frame_with_axis

    def get_frame_with_port(self, frame=None):
        frame = self.frame if frame is None else frame
        return self.get_frame_with_ray(frame, only_port=True)

    def get_frame_with_ray(self, frame=None, only_port=False):
        frame = self.frame if frame is None else frame
        imagePoints, jacobian = cv2.projectPoints(np.float32([[tracker_offset_x, tracker_offset_y, 0], [tracker_offset_x, tracker_offset_y, markerLength_tracker * 2]]), self.rvec_tracker, self.tvec_tracker, self.cameraMatrix, self.distCoeffs)
        frame_ = copy.copy(frame)
        if only_port:
            frame_with_ray = cv2.line(frame_, tuple(imagePoints[0][0]), tuple(imagePoints[0][0]), (255, 0, 0), 8)
        else:
            frame_with_ray = cv2.line(frame_, tuple(imagePoints[0][0]), tuple(imagePoints[1][0]), (255, 0, 0), 3)
        return frame_with_ray

    def get_plane(self, marker_id=-1, thickness=0):
        if(self.ids is None):
            self.error += 'No Marker '
            return self.NULL_POINT, None

        if marker_id not in self.ids:
            self.error += 'No Marker '
            return self.NULL_POINT, None

        idx = list(self.ids).index(marker_id)
        r_mat, _ = cv2.Rodrigues(self.rvecs[idx])
        t_vec = self.tvecs[idx]
        t_mat = np.array([t_vec[0], ] * 2).transpose()
        p_origin, p_norm = [0, 0, -1 * thickness], [0, 0, -1 * thickness + 1]
        line = np.transpose(np.array([p_origin, p_norm]))
        line_ = np.matmul(r_mat, line) + t_mat
        line_ = np.transpose(line_)
        planePoint = line_[0]
        planeNormal = (line_[1] - line_[0]) / np.linalg.norm(line_[1] - line_[0])
        return planePoint, planeNormal

    def get_ray(self):
        if self.ids_tracker is None:
            print('Error: Can not locate injection port !')
            self.error += 'No Port '
            return NULL_POINT, NULL_POINT
        r_mat, _ = cv2.Rodrigues(self.rvec_tracker)
        t_vec = self.tvec_tracker
        t_mat = np.array([t_vec, ] * 2).transpose()
        p_origin, p_norm = [tracker_offset_x, tracker_offset_y, 0], [tracker_offset_x, tracker_offset_y, 1]       # move offset
        line = np.transpose(np.array([p_origin, p_norm]))
        line_ = np.matmul(r_mat, line) + t_mat[0]
        line_ = np.transpose(line_)
        rayPoint = line_[0]
        rayDirection = (line_[1] - line_[0]) / np.linalg.norm(line_[1] - line_[0])
        return rayPoint, rayDirection

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

    def ray_intersect(self, marker_id, thickness=0):
        planeCenter, planeNormal = self.get_plane(marker_id, thickness)
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
                'tvec_tracker': self.tvec_tracker, 'rvec_tracker': self.rvec_tracker,
                'rvecs_tracker': self.rvecs_tracker, 'tvecs_tracker': self.tvecs_tracker,
                'corners_tracker': self.corners_tracker,
                'cameraMatrix': self.cameraMatrix, 'distCoeffs': self.distCoeffs,
                'error': self.error}
