import djitellopy as tello

class Drone():
  '''
  initialize the drone class
  '''
  def __init__(self):
    self.me = tello.Tello()
    self.me.connect()
    print("drone connect")
  