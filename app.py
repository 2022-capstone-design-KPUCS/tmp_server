import argparse

from flask import render_template, request
from flask_api import FlaskAPI

from lib.drone import Drone
from lib.camera import Camera

app = FlaskAPI(__name__)

def note_repr(key):
    return {
        'text': key
    }

@app.route('/', methods=['GET'])
def main():
  return render_template('index.html')

@app.route('/send_command', methods=['POST'])
def send_command():
    command = request.json['command']
    response = command
    return note_repr(response)


if __name__ == '__main__':
  #Initialize drone class
  drone = Drone()

  #camera for stream
  camera = Camera(drone)

  parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
  parser.add_argument("--port", default=5000, type=int, help="port number")
  args = parser.parse_args()
  app.run(host="0.0.0.0", port=args.port)