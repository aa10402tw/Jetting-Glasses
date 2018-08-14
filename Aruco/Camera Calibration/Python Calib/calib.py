####################################
### Need to use Python 3.5 build ###
####################################

import cv2
from cv2 import aruco
import yaml
import numpy as np
import copy
import PyCapture2


markerLength = 0.015
markerSeparation = 0.004

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_50)
board = aruco.GridBoard_create(1, 10, markerLength, markerSeparation, aruco_dict)
arucoParams = aruco.DetectorParameters_create()

camera = 'realtime'

# board_image = np.zeros((256, 256, 1), dtype="uint8")
# board_image = board.draw((1000, 2000))
# cv2.imwrite('board_tracker.jpg', board_image)
# cv2.waitKey(0)


def initRealtimeCamera():
    # set camera
    bus = PyCapture2.BusManager()
    cam = PyCapture2.Camera()
    uid = bus.getCameraFromIndex(0)
    cam.connect(uid)
    cam.startCapture()
    return cam


def capIm(cam):

    try:
        image = cam.retrieveBuffer()
    except PyCapture2.Fc2error as fc2Err:
        print("Error retrieving buffer :", fc2Err)
        return False, []
    row_bytes = float(len(image.getData())) / float(image.getRows())
    frame_gray = np.array(image.getData(), dtype="uint8").reshape((image.getRows(), image.getCols()))
    frame = cv2.cvtColor(frame_gray, cv2.COLOR_BAYER_BG2BGR)
    return True, frame


def Calibrate_camera(img_list):
    counter = []
    corners_list = []
    id_list = []
    first = True
    for im in img_list:
        img_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img_gray, aruco_dict, parameters=arucoParams)
        if first == True:
            corners_list = corners
            print(type(corners))
            id_list = ids
            first = False
        else:
            corners_list = np.vstack((corners_list, corners))
            id_list = np.vstack((id_list, ids))
        counter.append(len(ids))
    counter = np.array(counter)
    print("Calibrating camera .... Please wait...")
    #mat = np.zeros((3,3), float)
    ret, mtx, dist, rvecs, tvecs = aruco.calibrateCameraAruco(corners_list, id_list, counter, board, img_gray.shape, None, None)

    print("Camera matrix:\n", mtx, "\ndistCoeffs:\n", dist)
    return mtx, dist


if(camera == 'webcam'):
    cap = cv2.VideoCapture(0)
elif(camera == 'realtime'):
    cam = initRealtimeCamera()

img_list = []
show_axis = False
cameraMatrix, distCoeffs = None, None
while(True):
    if(camera == 'webcam'):
        ret, frame = cap.read()
    elif(camera == 'realtime'):
        ret, frame = capIm(cam)
    frame_ = copy.copy(frame)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame_, aruco_dict, parameters=arucoParams)

    frame_ = aruco.drawDetectedMarkers(frame_, corners, ids, (0, 255, 0))
    if show_axis:
        rvecs, tvecs, corners = aruco.estimatePoseSingleMarkers(corners, markerLength, cameraMatrix, distCoeffs)
        if(ids is not None):
            for i, id in enumerate(ids):
                if(id < 5 or id >= 45):
                    frame_ = cv2.aruco.drawAxis(frame_, cameraMatrix, distCoeffs, rvecs[i], tvecs[i], markerLength)
    cv2.putText(frame_, 'Press "a" to add img', (30, 25), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1)
    cv2.putText(frame_, 'Press "c" to calib', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1)
    cv2.putText(frame_, 'Press "q" to exit', (30, 75), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 1)
    cv2.putText(frame_, '#imgs:%i' % len(img_list), (400, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('frame', frame_)
    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
        break
    elif c & 0xFF == ord('a'):
        img_list.append(frame)
    elif c & 0xFF == ord('c'):
        cameraMatrix, distCoeffs = Calibrate_camera(img_list)
        show_axis = True


cv2.destroyAllWindows()

if(camera == 'webcam'):
    file_name = "CalibResult/calibration_webcam.yaml"
    cap.release()
elif(camera == 'realtime'):
    file_name = "CalibResult/calibration_realtime.yaml"

data = {'camera_matrix': np.asarray(cameraMatrix).tolist(), 'dist_coeff': np.asarray(distCoeffs).tolist()}
with open(file_name, "w") as f:
    yaml.dump(data, f)
