
class Camera(object):
  '''
  camera class that can access Tello camera
  1. computer is connected to Tello's Wifi network
  2. send "command" and "streamon" before being able to access the stream
  '''
  def __init__(self, drone):
    self.drone = drone