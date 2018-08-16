import numpy as np

markerLength = 0.012

markerLength_tracker = 0.14 / 10 / 11 * 10
markerSeparation_tracker = 0.14 / 10 / 11

tracker_id_left = 45
tracker_id_right = 40
offset_left = -5 * 1.25
offset_right = 5 * 1.25

tracker_offset_x = markerLength_tracker * 0.5
tracker_offset_y = (markerLength_tracker + markerSeparation_tracker) * 9 + markerLength_tracker * 0.5

NULL_POINT = [np.nan, np.nan, np.nan]

COLOR_CORNER = [[0, 0, 0, 0.75]]
COLOR_TRACKER = [[0, 1, 0, 0.75]]
COLOR_CAMERA = [[0, 0, 0, 0.25]]
