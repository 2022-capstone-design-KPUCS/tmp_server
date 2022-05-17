import firebase_admin
from datetime import datetime
from firebase_admin import credentials
from firebase_admin import messaging


def send_message(type: str):
    
    # TODO: App Device 고유 토큰, 해당 토큰을 앱에서 호출하는 것 구현해야됨
    registration_token = 'dEBqvE2KQeGI3Dy81RPxN4:APA91bEN76BjChlIRlQuLg2vHp8E_jH2mIk0LzuCbiVhrLElHr2loyVa0IITEY0S4pP0j9nbupDysrnoH9EWFO2gWjwIF9KS7cqY9tGUVcaS5Whmtk3EYnrW0-Hx9bIMqoH5DxhoqyUV'
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
    # default_app = firebase_admin.initialize_app(cred, name="Firedrone")
    send_message("FIRE")