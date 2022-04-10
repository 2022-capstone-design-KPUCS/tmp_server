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
