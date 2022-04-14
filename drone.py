from threading import Thread
from flask import jsonify, request
from flask_restx import Resource, Namespace

import lib.autopilot as ap
from lib.tello import init_drone, drone_control, detect_fire

Drone = Namespace('Drone')

drone_dict = {}

@Drone.route('/init')
class TelloInit(Resource):
  def get(self):
    drone = init_drone()
    serial_num = drone.query_serial_number()

    if serial_num in drone_dict:
      message = "already exist"
    else:
      drone_dict[serial_num] = drone
      message = "connect success"

    return {
      "serial_number": serial_num,
      "message": message
    }

@Drone.route('/<string:drone_id>')
class Tello(Resource):
  def get(self, drone_id):
    global drone_dict

    battery = drone_dict[drone_id].get_battery()
    return {
      "battery": battery
    }

  def post(self, drone_id):
    post_data = request.get_json()
    if post_data['data'] == 'make_command':
      ap.make_command()
      
    return {
      "messange": "command.txt file made",
    }, 200


@Drone.route('/<string:drone_id>/detect')
class TelloMission(Resource):
  def get(self, drone_id):
    global drone_dict
    print("COMEONE")
    drone = drone_dict[drone_id]
    stream = Thread(target=detect_fire(drone))
    stream.start()
    drone_control(drone)
    stream.join()

    return {
      "drone_id": drone_id
    }