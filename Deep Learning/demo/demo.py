import numpy as np
import cv2

import random
import math

import torch 
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.autograd import Variable

LABELS = [
    'index_1', 'index_2', 'index_3',
    'middle_1', 'middle_2', 'middle_3',
    'ring_1', 'ring_2', 'ring_3',
    'little_1', 'little_2', 'little_3',
    'palm', 'background'
]

output_video = False
if output_video:
	out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,480))

def predict_frame(model, frame, LABELS):
    image = cv2.resize(frame, (300,300))
    image = image.astype('float32') / 255.0
    x = np.rollaxis(image, 2, 0)
    x = torch.from_numpy( np.array([x]) )
    out_pred = model(x)
    prob, y_pred = torch.max(out_pred, 1)
    return LABELS[y_pred], math.exp(prob)

class MyCNN(nn.Module):
    def __init__(self, num_class):
        super(MyCNN, self).__init__()
        # conv_1
        self.conv_1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2), 
            # input shape (3, 100, 100), output shape (16, 50, 50)
        )
        # conv_2
        self.conv_2 = nn.Sequential(
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2), 
            # input shape (16, 50, 50), output shape (32, 25, 25)
        ) 
        # output
        self.fc_1 = nn.Linear(in_features=32 * 75 * 75, out_features=128) 
        self.fc_2 = nn.Linear(in_features=128, out_features=num_class)
        self.num_class = num_class

    def forward(self, x):
        x = self.conv_1(x)
        x = self.conv_2(x)
        x = x.view(x.size(0), -1)  # flatten the output of conv2 to (batch_size, 32 * 25 * 25)
        x = F.relu(self.fc_1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc_2(x)
        return F.log_softmax(x)        




# cap = cv2.VideoCapture(0)
# flag, cur_frame = cap.read()
cap_1 = cv2.VideoCapture(1)
cap_2 = cv2.VideoCapture(2)
flag, cur_frame_1 = cap_1.read()
flag, cur_frame_2 = cap_2.read()

# model = torch.load('model.pkl')

model = MyCNN(num_class=len(LABELS))
model.cpu()
model.load_state_dict(torch.load('model_params.pkl'))

while(True):
    # flag, frame = cap.read()
    # frame[235:245, 315:325, :] = (255,0,0)
    flag, frame_1 = cap_1.read()
    flag, frame_2 = cap_2.read()
    frame = np.concatenate((frame_1, frame_2), axis=1)
	
    label, prob = predict_frame(model, frame, LABELS)

    frame_1[235:245, 315:325, :] = (255,0,0)
    frame = np.concatenate((frame_1, frame_2), axis=1)

    cv2.putText(frame, "%s (%.2f %%)" %(str(label), prob*100), (50,50), 0, 1, (255,0,0),3)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if output_video:
        out.write(frame)
# cap.release()
cap_1.release()
cap_2.release()
cv2.destroyAllWindows()