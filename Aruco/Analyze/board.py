####################################
### Need to use Python 3.5 build ###
####################################
import os
import cv2
import numpy as np
from cv2 import aruco

nMarkers, markerSize, randomSeed = 10, 3, 10
markerLength, markerSeparation = 0.02, 0.005


class ArucoBoard:
    def __init__(self, nMarkers=8, markerSize=3, markerLength=0.012, markerSeparation=0.003, randomSeed=10, size=(0, 0)):
        self.aruco_dict = aruco.custom_dictionary(nMarkers, markerSize, randomSeed)
        if size == (0, 0):
            self.size = (1, nMarkers)
            self.board = aruco.GridBoard_create(1, nMarkers, markerLength, markerSeparation, self.aruco_dict)
        else:
            self.size = size
            self.board = aruco.GridBoard_create(size[0], size[1], markerLength, markerSeparation, self.aruco_dict)

    def getBoard(self):
        return self.board

    def getBoardSize(self):
        return self.size

    def getDict(self):
        return self.aruco_dict

    def getBoardImage(self, size=(1000, 2000)):
        board_image = np.zeros((256, 256, 1), dtype="uint8")
        board_image = self.board.draw(size)
        return board_image

    def saveBoardImage(self, img_name='board_tracker.jpg'):
        cv2.imwrite(img_name, self.getBoardImage())
        cv2.imshow('', cv2.resize(self.getBoardImage(), (300, 600)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


##################
## For Tracker ###
##################
if __name__ == '__main__':
    # arucoTrackerBoard = ArucoBoard(nMarkers=8, markerSize=3, markerLength=0.012, markerSeparation=0.003, randomSeed=10)
    arucoTrackerBoard = ArucoBoard(nMarkers=10, markerSize=3, markerLength=0.012, markerSeparation=0.0012, randomSeed=10, size=(1, 10))
    arucoMarkerBoard = ArucoBoard(nMarkers=20, markerSize=3, markerLength=0.012, markerSeparation=0.003, randomSeed=1, size=(2, 10))
    arucoTrackerBoard.saveBoardImage(img_name='TrackerBoard.jpg')
    arucoMarkerBoard.saveBoardImage(img_name='MarkerBoard.jpg')
    print('TrackerBoard:', 1.7 * 8)
    print('MarkerBoard:', 1.5 * 9)
    help(aruco.custom_dictionary)
