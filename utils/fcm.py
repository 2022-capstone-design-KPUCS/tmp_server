import firebase_admin
from datetime import datetime
from firebase_admin import credentials
from firebase_admin import messaging
# from utils.login import get_token
from login import get_token
from flight import get_route

def send_message(type: str):
    # cred = credentials.Certificate("C:/Users/owner/Desktop/oo/drone-api-90997-firebase-adminsdk-xuc2p-122f502f56.json")
    cred = credentials.Certificate("/Users/seanhong/Developer/CapstoneDesign/drone-api-90997-firebase-adminsdk-xuc2p-122f502f56.json")
    default_app = firebase_admin.initialize_app(cred)
    # username, password = map(str, input("Please Enter admin ID: ").split())
    registration_token, auth_token = get_token("seanhong2000", "Suskyssc2")
    location = get_route()
    message = messaging.Message(
        data={
            'type': type,
            'time': str(datetime.now())
        },
        android=messaging.AndroidConfig(
            data={
                'type': type,
                'time': str(datetime.now()),
                'token': str(auth_token),
                'lat': str(location[0]['lat']),
                'lng': str(location[0]['lng'])
            },
            notification=messaging.AndroidNotification(click_action=".activities.Notification")
        ),
        notification=messaging.Notification(title=type, body=str(datetime.now())),
        token=registration_token
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)


if '__main__' == __name__:
    send_message("Fire")
