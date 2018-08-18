import sys
sys.path.insert(0, './lib')
from NatNetClient import NatNetClient
from cv2 import aruco
import pandas as pd

# This is a callback function that gets connected to the NatNet client and called once per mocap frame.

cur_optiTrack_pos = (0, 0, 0)

optiTrack_pos_list = []
camera_pos_list = []


def receiveNewFrame(frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                    labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged):
    # print("Received frame", frameNumber)
    x = 0
    # This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame


def receiveRigidBodyFrame(id, position, rotation):
    global cur_optiTrack_pos
    if(id == 1):
        cur_optiTrack_pos = position
        optiTrack_pos_list.append(cur_optiTrack_pos)
    #print("Received frame for rigid body", id, position, rotation)



# This will create a new NatNet client
streamingClient = NatNetClient(server="192.168.0.136")

# Configure the streaming client to call our rigid body handler on the emulator to send data out.
streamingClient.newFrameListener = receiveNewFrame
streamingClient.rigidBodyListener = receiveRigidBodyFrame

# Start up the streaming client now that the callbacks are set up.
# This will run perpetually, and operate on a separate thread.
streamingClient.run()

from jettingGlasses import *
from cameraParams import *

camera = 'webcam'
cameraMatrix, distCoeffs = loda_camera_params(camera=camera)

JG = Jetting_Glasses(cameraMatrix, distCoeffs, need_acc=True)
draw = Draw3D()
cap = cv2.VideoCapture(0)

target_id = 5

while True:
    ret, frame = cap.read()
    JG.update_frame(frame)
    frame = JG.get_frame(frame, corner=True)
    frame_info = JG.get_frame_info()
    ids, rvecs, tvecs = frame_info['ids'], frame_info['rvecs'], frame_info['tvecs']

    if ids is not None:
        if target_id in ids:
            idx = list(ids).index(target_id)
            rvec, tvec = frame_info['rvecs'][idx], frame_info['tvecs'][idx]
            optiTrack_pos_list.append(list(cur_optiTrack_pos))
            camera_pos_list.append(tvec[0])
            print('optiTrack:', list(cur_optiTrack_pos))
            print('webcam:', tvec[0])

    cv2.imshow('frame', frame)  # check ray
    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):  # 按 q 键退出
        break

streamingClient.stop()
cv2.destroyAllWindows()
cap.release()


df = pd.DataFrame({'point_OptiTrack': optiTrack_pos_list, 'point_Camera': camera_pos_list})
df.to_csv('./CalibResult/TwoCoordinatePoints.csv', sep='\t', index=False)

# draw.track(camera_pos_list)
# draw.show()
# draw.__init__()
# draw.track(optiTrack_pos_list)
# draw.show()
