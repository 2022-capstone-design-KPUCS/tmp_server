import requests
import json
from urllib.parse import urljoin

def get_route():
    # username, password = map(str, input("Please Enter admin ID: ").split())
    post = "http://ec2-3-38-108-184.ap-northeast-2.compute.amazonaws.com:8000/auth/token/login/"
    data = {
        "username": "seanhong2000",
        "password": "Suskyssc2"
    }
    res = requests.post(post, data=data)
    auth_token = json.loads(res.text)["auth_token"]
    BASEURL = "http://ec2-3-38-108-184.ap-northeast-2.compute.amazonaws.com:8000/api/v1/"
    FLIGHTAPI = "flights/"
    HEADER = {
        "Authorization": "Token " + auth_token
    }
    flight_content = requests.get(urljoin(base=BASEURL, url=FLIGHTAPI), headers=HEADER).text
    path = json.loads(flight_content)["results"][0]["flight_path"]
    return path
    

if '__main__' == __name__:
    get_route()