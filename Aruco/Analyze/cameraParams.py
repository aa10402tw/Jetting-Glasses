import yaml
import numpy as np
import cv2
import numpy as np
import PyCapture2


def get_resolution(camera):
    if camera == 'webcam':
        return (640, 480)
    elif camera == 'realtime':
        return (1920, 1200)


def loda_camera_params(camera='webcam'):

    if camera == 'webcam':
        file_name = "CamParams/calibration_webcam.yaml"
    elif(camera == 'usb'):
        file_name = "CalibResult/calibration_usb.yaml"
    elif camera == 'realtime':
        file_name = "CamParams/calibration_realtime.yaml"
    else:
        print('error: no such camera')

    with open(file_name, 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as error:
            print(error)
    return np.array(data['camera_matrix']), np.array(data['dist_coeff'])


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


class MyCam:
    def __init__(self, camera='webcam'):
        self.camera = camera
        if self.camera == 'webcam':
            self.cap = cv2.VideoCapture(0)
            ret, frame = self.cap.read()
        elif(camera == 'usb'):
            self.cap = cv2.VideoCapture(1)
            ret, frame = self.cap.read()
        elif self.camera == 'realtime':
            self.cam = initRealtimeCamera()
            ret, frame = capIm(self.cam)

    def get_frame(self):
        if self.camera == 'webcam':
            return self.cap.read()
        elif self.camera == 'usb':
            return self.cap.read()
        elif self.camera == 'realtime':
            return capIm(self.cam)

    def release(self):
        self.cap.release()
