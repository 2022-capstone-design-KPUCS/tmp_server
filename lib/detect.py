from threading import Thread

def detect_and_move(object):
  stream = Thread(object.detect_fire())
  stream.start()
  object.drone_control()
  stream.join()