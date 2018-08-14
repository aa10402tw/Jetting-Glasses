import cv2
from cv2 import aruco
import yaml
import numpy as np
import copy
import PyCapture2

camera = 'webcam'


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


def calib(img_list):

    n_rows = 5
    n_cols = 4
    n_cols_and_rows = (n_cols, n_rows)  # originally (7,6) # 4,5 same results
    n_rows_and_cols = (n_rows, n_cols)
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((n_rows * n_cols, 3), np.float32)
    objp[:, :2] = np.mgrid[0:n_rows, 0:n_cols].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    for i, img in enumerate(img_list):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, n_rows_and_cols, None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, n_rows_and_cols, corners, ret)
            cv2.imshow('img', cv2.resize(img, (640, 480)))
            cv2.waitKey(500)

    cv2.destroyAllWindows()
    print('Calibrating...')
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None, flags=(cv2.CALIB_FIX_PRINCIPAL_POINT
                                                                                                                  + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_THIN_PRISM_MODEL))

    mean_error = 0
    tot_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        tot_error += error

    print("mean error: ", tot_error / len(objpoints))

    return mtx, dist


if(camera == 'webcam'):
    cap = cv2.VideoCapture(0)
elif(camera == 'usb'):
    cap = cv2.VideoCapture(1)
elif(camera == 'realtime'):
    cam = initRealtimeCamera()

img_list = []
cameraMatrix, distCoeffs = None, None

while(True):
    if(camera == 'webcam'):
        ret, frame = cap.read()
    elif(camera == 'realtime'):
        ret, frame = capIm(cam)
    frame_ = copy.copy(frame)
    frame_ = cv2.resize(frame_, (640, 480))
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
        mtx, dist = calib(img_list)


if(camera == 'webcam'):
    file_name = "CalibResult/calibration_webcam.yaml"
    cap.release()
elif(camera == 'usb'):
    file_name = "CalibResult/calibration_usb.yaml"
elif(camera == 'realtime'):
    file_name = "CalibResult/calibration_realtime.yaml"

print(mtx)
print(dist)

data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}
with open(file_name, "w") as f:
    yaml.dump(data, f)
