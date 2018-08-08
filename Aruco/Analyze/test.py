####################################
### Need to use Python 3.5 build ###
####################################
import os
import cv2
import numpy as np
import PyCapture2


def capIm():
    try:
        img = cam.retrieveBuffer()
    except PyCapture2.Fc2error as fc2Err:
        print("Error retrieving buffer :", fc2Err)
        return False, []

    data = np.array(img.getData(), dtype=np.uint8)
    data = data.reshape((img.getRows(), img.getCols()))

    return True, data


while cv2.waitKey(1) & 0xFF != 27:
    ret, im = capIm()
    if not ret:
        break

    ret = cv2.getTrackbarPos('SHUTTER', 'PyCapImg')
    if ret / 40 != SHUTTER:
        SHUTTER = ret
        cam.stopCapture()
        cam.setProperty(type=PyCapture2.PROPERTY_TYPE.SHUTTER, absValue=SHUTTER / 40)
        cam.startCapture()

    ret = cv2.getTrackbarPos('GAIN', 'PyCapImg')
    if ret / 20 != GAIN:
        GAIN = ret
        cam.stopCapture()
        cam.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, absValue=GAIN / 20)
        cam.startCapture()

    sh = cam.getProperty(PyCapture2.PROPERTY_TYPE.SHUTTER)
    ga = cam.getProperty(PyCapture2.PROPERTY_TYPE.GAIN)
    cv2.displayOverlay('PyCapImg', 'SHUTTER:{:.2f}, GAIN:{:.2f}'.format(sh.absValue, ga.absValue))

    cv2.imshow('PyCapImg', im)


# 設定をもとに戻しておく
cam.stopCapture()
fmt7imgSet = PyCapture2.Format7ImageSettings(0, 0, 0, fmt7info.maxWidth, fmt7info.maxHeight, pxfmt)
fmt7pktInf, isValid = cam.validateFormat7Settings(fmt7imgSet)
cam.setFormat7ConfigurationPacket(fmt7pktInf.recommendedBytesPerPacket, fmt7imgSet)
cam.setProperty(type=PyCapture2.PROPERTY_TYPE.SHUTTER, autoManualMode=True)
cam.setProperty(type=PyCapture2.PROPERTY_TYPE.GAIN, autoManualMode=True)
cam.setProperty(type=PyCapture2.PROPERTY_TYPE.SHARPNESS, onOff=True)
cam.disconnect()

cv2.destroyAllWindows()

try:
    os.remove('tmp.bmp')
except:
    pass
