from flask_restx import Resource, Namespace
from flask import Response
import lib.autopilot as ap
from lib.tello import init_drone, detect_fire, drone_control, stop_flight
from lib.autopilot import make_command,distance
from threading import Thread
from multiprocessing import Process


Drone = Namespace('Drone')
drone = init_drone()

@Drone.route('test')
class test(Resource):
  def get(self):
    stop_flight()

@Drone.route('/autopilot')
class AutoPilot(Resource):
  def get(self):
    make_command(distance)

@Drone.route('/detect')
class TelloDetect(Resource):
  def get(self):
    return Response(detect_fire(drone), mimetype='multipart/x-mixed-replace; boundary=frame')
    