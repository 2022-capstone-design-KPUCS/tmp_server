from flask_restx import Resource, Namespace
from flask import Response
import lib.autopilot as ap
from lib.tello import init_drone, detect_fire, drone_control
from threading import Thread
from multiprocessing import Process


Drone = Namespace('Drone')
#drone = init_drone()
drone = 'drone'

@Drone.route('/control')
class TelloControl(Resource):
  def get(self):
    drone_control(drone)

@Drone.route('/detect')
class TelloDetect(Resource):
  def get(self):
    return Response(detect_fire(drone), mimetype='multipart/x-mixed-replace; boundary=frame')
    