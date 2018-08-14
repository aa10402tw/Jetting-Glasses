import cv2
import numpy as np
import PyCapture2


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
        elif self.camera == 'realtime':
            self.cam = initRealtimeCamera()
            ret, frame = capIm(self.cam)

    def get_frame(self):
        if self.camera == 'webcam':
            return self.cap.read()
        elif self.camera == 'realtime':
            return capIm(self.cam)

    def get_resolution(self):
        if self.camera == 'webcam':
            return (640, 480)
        elif self.camera == 'realtime':
            return (1920, 1200)

    def release(self):
        if self.camera == 'webcam':
            self.camera.release()
