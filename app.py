import argparse
from flask import Flask
from flask_restx import Api
from drone import Drone
from notification import Notification

app = Flask(__name__)
api = Api(app)

api.add_namespace(Drone, '/drone')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
  parser.add_argument("--port", default=5000, type=int, help="port number")
  args = parser.parse_args()
  app.run(host="0.0.0.0", port=args.port)

