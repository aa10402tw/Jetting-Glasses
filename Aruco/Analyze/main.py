####################################
### Need to use Python 3.5 build ###
####################################


# TODO : Change Drawing Ray

from jettingGlasses import *
from cameraParams import *

camera = 'webcam'

cameraMatrix, distCoeffs = loda_camera_params(camera=camera)
# cameraMatrix = np.reshape(cameraMatrix, (3, 3))
# distCoeffs = np.reshape(distCoeffs, (1, 5))
# mode = 'image'
mode = 'video'

JG = Jetting_Glasses(cameraMatrix, distCoeffs, need_acc=True)
draw = Draw3D()

######################
### Static Image  ####
######################
if mode == 'image':

    # Update frame
    frame = cv2.imread('TestImges/1.jpg')
    JG.update_frame(frame)

    # Compute
    frame_info = JG.get_frame_info()
    rayPoint, planeCenter, intersectPoint, dis = JG.ray_intersect(marker_id=20)

    # Show Frame
    frame = JG.get_frame(frame, corner=True, axis=True, port=False, ray=False)
    cv2.imshow('frame', frame)
    cv2.imshow('frame', cv2.resize(frame, (1080, 720)))
    cv2.waitKey(0)

    # Draw In 3D
    draw.camera()
    draw.corner(frame_info)
    draw.port_ray(frame_info)
    draw.intersect(planeCenter, intersectPoint)
    # draw.adjust_lim(intersectPoint, rayPoint)
    draw.show()


# ######################
# ### Dynamic Video ####
# ######################
if mode == 'video':
    # Check
    myCam = MyCam(camera)
    while(True):
        # capture frame-by-frame
        ret, frame = myCam.get_frame()
        JG.update_frame(frame)
        frame = JG.get_frame(frame, corner=True, axis=True, tracker_corner=True, port=True, ray=True)
        frame = JG.get_frame_with_board(frame)
        cv2.imshow('frame', frame)  # check ray
        c = cv2.waitKey(1)
        if c & 0xFF == ord('q'):  # 按 q 键退出
            break
        if c & 0xFF == ord('w'):  # 按 w to view 3D
            cv2.waitKey(3000)
            frame_info = JG.get_frame_info()
            rayPoint, planeCenter, intersectPoint, dis = JG.ray_intersect(marker_id=40)
            # Draw In 3D
            draw.camera()
            draw.corner(frame_info)
            draw.tracker_corner(frame_info)
            draw.port_ray(frame_info)
            draw.intersect(planeCenter, intersectPoint)
            draw.show()
            draw.__init__()

    # when everything done , release the capture
    myCam.release()
    cv2.destroyAllWindows()
