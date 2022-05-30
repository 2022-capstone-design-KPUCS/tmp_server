import requests
import json
from urllib.parse import urljoin
from login import get_token

def get_route():
    username, password = map(str, input("Please Enter admin ID: ").split())
    post = "http://localhost:8000/auth/token/login/"
    data = {
        "username": username,
        "password": password
    }
    res = requests.post(post, data=data)
    auth_token = json.loads(res.text)["auth_token"]
    BASEURL = "http://localhost:8000/api/v1/"
    FLIGHTAPI = "flights/"
    HEADER = {
        "Authorization": "Token " + auth_token
    }
    flight_content = requests.get(urljoin(base=BASEURL, url=FLIGHTAPI), headers=HEADER).text
    path = json.loads(flight_content)["results"][0]["flight_path"]
    return path
    

if '__main__' == __name__:
    get_route()