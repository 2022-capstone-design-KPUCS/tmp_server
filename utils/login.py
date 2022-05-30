import requests
import json 

def get_token(username, password):
    post = "http://localhost:8000/auth/token/login/"
    data = {
        "username": username,
        "password": password
    }
    res = requests.post(post, data=data)
    auth_token = json.loads(res.text)["auth_token"]
    header = {
        "Authorization": "Token " + auth_token
    }
    get = "http://localhost:8000/api/v1/user/"
    res = requests.get(url=get, headers=header)
    results = json.loads(res.text)["results"]
    for res in results:
        if res["auth_token"] == auth_token:
            return res["token"]
