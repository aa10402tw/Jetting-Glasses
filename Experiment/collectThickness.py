############################
### Use Python 3.5 Build ###
############################

import warnings
warnings.filterwarnings("ignore")

import tkinter as tk
from PIL import ImageTk, Image, ImageDraw
import numpy as np
import time
import cv2
import pandas as pd
import os
import multiprocessing
import pickle


pos2thick = {}
user_name = ''

print()
with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)
