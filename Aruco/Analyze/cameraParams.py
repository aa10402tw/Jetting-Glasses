import yaml
import numpy as np


def loda_camera_params(camera='webcam'):

    if camera == 'webcam':
        file_name = "CamParams/calibration_webcam.yaml"
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
