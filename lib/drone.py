import djitellopy as tello
import torch
import numpy as np
import cv2
import requests
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import Annotator

from autopilot import make_command

import aws_s3

DEST_URL = 'http://localhost:8000/api/v1'
# model env
MODEL_PATH = 'runs/train/exp4/weights/e50b32.pt'
img_size = 416
conf_thres = 0.5  # confidence threshold
iou_thres = 0.45  # NMS IOU threshold
max_det = 1000  # maximum detections per image
classes = None  # filter by class
agnostic_nms = False  # class-agnostic NMS

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

ckpt = torch.load(MODEL_PATH, map_location=device)
model = ckpt['ema' if ckpt.get('ema') else 'model'].float().fuse().eval()
class_names = ['fire'] # model.names
stride = int(model.stride.max())
colors = ((0, 255, 0)) # (gray, red, green)

class Drone():
  '''
  initialize the drone class
  function that drone can do
  '''
  def __init__(self):
    make_command()
    self.s3 = aws_s3.s3_connection()
    self.me = tello.Tello()
    self.me.connect()

  @staticmethod
  def send_format(type):
    '''
    0 : fire
    1 : smoke
    '''
    return {'data_type:', type}
  
  @classmethod
  def upload_s3(self, file_name):
    '''
    upload img to s3
    '''
    bucket_name = "sangwoha-bucket"
    aws_s3.s3_put_object(self.s3, bucket_name, file_name)
    return
  
  @classmethod
  def get_drone_battery(self):
    '''
    return drone battery
    '''
    return self.me.get_battery()
  
  @classmethod
  def drone_control(self):
    '''
    move auto with thread
    command in command.txt
    '''
    f= open('./command.txt', 'r')
    command=f.readlines()
    for i in command:
        if i == "takeoff\n":
            self.me.takeoff()

        elif i[:5] =="speed":
            speed=int(i[6:])
            self.me.set_speed(speed)
        elif i[:3] =="ccw":
            angle=int(i[4:])
            self.me.rotate_counter_clockwise(angle)

        elif i[:2] =="cw":
            angle=int(i[3:])
            self.me.rotate_clockwise(angle)
        elif i[:7] == "forward":
            distance=int(i[8:])
            self.me.move_forward(distance)

        elif i == "land\n":
            self.me.land()

  @classmethod
  def stream_with_yolo(self):
    self.me.streamon()
    cap = self.me.get_frame_read()
    while True:

      if cv2.waitKey(1) == ord('q'):
        break

      img = cap.frame

      # preprocess
      img_input = letterbox(img, img_size, stride=stride)[0] # padding
      img_input = img_input.transpose((2, 0, 1))[::-1] # BGR to RGB
      img_input = np.ascontiguousarray(img_input) 
      img_input = torch.from_numpy(img_input).to(device) # torch Tensor형식 변환
      img_input = img_input.float()
      img_input /= 255.
      img_input = img_input.unsqueeze(0)

      # inference
      pred = model(img_input, augment=False, visualize=False)[0]

      # postprocess
      pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)[0]

      pred = pred.cpu().numpy()

      pred[:, :4] = scale_coords(img_input.shape[2:], pred[:, :4], img.shape).round() # img size에 맞게 rescailing

      annotator = Annotator(img.copy(), line_width=3, example=str(class_names), font='data/malgun.ttf')

      for p in pred:
          class_name = class_names[int(p[5])]

          x1, y1, x2, y2 = p[:4]
          
          # detect fire or smoke
          if p[5]:
            r = requests.post(url=DEST_URL, data = self.send_format(p[5]))
          
          annotator.box_label([x1, y1, x2, y2], '%s %d' % (class_name, float(p[4]) * 100), color=colors[int(p[5])])

      result_img = annotator.result()

      # 이미지 정보를 s3에 보내주기.
      self.upload_s3(img_input)

      cv2.imshow('result', result_img)

    cap.release()