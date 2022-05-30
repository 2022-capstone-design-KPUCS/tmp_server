import firebase_admin
from datetime import datetime
from firebase_admin import credentials
from firebase_admin import messaging
from login import get_token

def send_message(type: str):
    username, password = map(str, input("Please Enter admin ID: ").split())
    registration_token = get_token(username, password)
    message = messaging.Message(
        data={
            'type': type,
            'time': str(datetime.now())
        },
        notification=messaging.Notification(title=type, body=str(datetime.now())),
        token=registration_token
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)

if '__main__' == __name__:
    cred = credentials.Certificate("/Users/seanhong/Developer/CapstoneDesign/drone-api-90997-firebase-adminsdk-xuc2p-122f502f56.json")
    default_app = firebase_admin.initialize_app()
    default_app = firebase_admin.initialize_app(cred, name="Firedrone")
    send_message("FIRE")
