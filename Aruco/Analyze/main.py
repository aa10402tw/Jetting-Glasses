####################################
### Need to use Python 3.6 build ###
####################################

from jettingGlasses import*
from cameraParams import *

cameraMatrix, distCoeffs = loda_camera_params(camera='realtime')
cameraMatrix = np.array([[4.10962841e+03, 0.00000000e+00, 7.58504000e+02],
                         [0.00000000e+00, 4.08826624e+03, 4.69926783e+02],
                         [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
distCoeffs = np.array([[-2.13437467e+00, 7.02947886e+01, - 6.50519802e-02, - 2.35705530e-02, - 1.29424669e+03]])
cameraMatrix = np.reshape(cameraMatrix, (3, 3))
distCoeffs = np.reshape(distCoeffs, (1, 5))
mode = 'image'
# mode = 'video'

######################
### Static Image  ####
######################
if mode == 'image':
    # Initq
    JG = Jetting_Glasses(cameraMatrix, distCoeffs)
    draw = Draw3D()

    # Update frame
    frame = cv2.imread('TestImges/1.jpg')
    JG.update_frame(frame)

    # Compute
    frame_info = JG.get_frame_info()
    rayPoint, planeCenter, intersectPoint, dis = JG.ray_intersect(marker_id=34)

    # Show Frame
    frame = JG.get_frame(frame, corner=True, axis=True, port=True, ray=True)
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
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    JG = Jetting_Glasses(cameraMatrix, distCoeffs)
    draw = Draw3D()
    while(True):
        # capture frame-by-frame
        ret, frame = cap.read()
        JG.update_frame(frame)
        frame = JG.get_frame_with_corner(frame)
        frame = JG.get_frame_with_axis(frame)
        frame = JG.get_frame_with_port(frame)
        cv2.imshow('frame', JG.get_frame_with_ray(frame))  # check ray
        c = cv2.waitKey(1)
        if c & 0xFF == ord('q'):  # 按q键退出
            break
        if c & 0xFF == ord('w'):  # 按q键退出
            cv2.waitKey(3000)
            frame_info = JG.get_frame_info()
            rayPoint, planeCenter, intersectPoint, diqs = JG.ray_intersect(marker_id=9)
            # Draw In 3D
            draw.camera()
            draw.corner(frame_info)
            draw.port_ray(frame_info)
            draw.intersect(planeCenter, intersectPoint)

            draw.show()

    # when everything done , release the capture
    cap.release()
    cv2.destroyAllWindows()
