import djitellopy as tello
import torch
import numpy as np
import cv2
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import Annotator
import requests

from drone import Drone

class Camera():
  '''
  camera class that can access Tello camera
  1. computer is connected to Tello's Wifi network
  2. send "command" and "streamon" before being able to access the stream
  '''
  def __init__(self):
    self.drone = Drone()
  
  def start_detecting(self):
    self.drone.stream_with_yolo()
