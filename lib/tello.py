from pickle import TRUE
import djitellopy as tello
import torch
import numpy as np
import cv2
import threading
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import Annotator
from utils.fcm import send_message
import threading


Fire=False
isFireDetected = False

MODEL_PATH = 'runs/train/exp4/weights/e50b32.pt'
img_size = 416
conf_thres = 0.5
iou_thres = 0.45
max_det = 1000
classes = None
agnostic_nms = False

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
ckpt = torch.load(MODEL_PATH, map_location=device)
model = ckpt['ema' if ckpt.get('ema') else 'model'].float().fuse().eval()
class_names = ['fire']
stride = int(model.stride.max())
colors = ((0, 255, 0))

Fire=False

def init_drone():
    drone = tello.Tello()
    drone.connect()
    return drone


def drone_control(object):
    f = open('./command.txt', 'r')
    command = f.readlines()
    for i in command:
        if Fire==True:
            stop_flight(object)    
            break
        if i == "takeoff\n":
            object.takeoff()

        elif i[:5] == "speed":
            speed = int(i[6:])
            object.set_speed(speed)

        elif i[:3] == "ccw":
            angle = int(i[4:])
            object.rotate_counter_clockwise(angle)

        elif i[:2] == "cw":
            angle = int(i[3:])
            object.rotate_clockwise(angle)

        elif i[:7] == "forward":
            distance = int(i[8:])
            object.move_forward(distance)

        elif i == "land\n":
            object.land()


def stop_flight(object):
    send_message("Fire")
    object.send_control_command('stop')
    


def detect_fire(object):
    object.streamon()
    cap = object.get_frame_read()
    cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
    t1=threading.Thread(target=drone_control,args=(object,))
    t1.start()
    while True:
        if cv2.waitKey(1) == ord('q'):
            break
        img = cap.frame
        

        # preprocess
        img_input = letterbox(img, img_size, stride=stride)[0]  # padding
        img_input = img_input.transpose((2, 0, 1))[::-1]  # BGR to RGB
        img_input = np.ascontiguousarray(img_input)
        img_input = torch.from_numpy(img_input).to(device)  # torch Tensor형식 변환
        img_input = img_input.float()
        img_input /= 255.
        img_input = img_input.unsqueeze(0)

        # inference
        pred = model(img_input, augment=False, visualize=False)[0]

        # postprocess
        pred = non_max_suppression(
            pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)[0]
        pred = pred.cpu().numpy()
        # img size에 맞게 rescailing
        pred[:, :4] = scale_coords(
            img_input.shape[2:], pred[:, :4], img.shape).round()
        annotator = Annotator(img.copy(), line_width=3, example=str(
            class_names), font='data/malgun.ttf')
        #print(pred)
        for p in pred:
            class_name = class_names[int(p[5])]
            """ 화재 감지 시 사용자에게 알림 문자 """
            if int(p[5]) == 0:
                global Fire
                Fire=True
            print(p[5])

            x1, y1, x2, y2 = p[:4]
            annotator.box_label([x1, y1, x2, y2], '%s %d' % (
                class_name, float(p[4]) * 100), color=colors[int(p[5])])

            # if int(p[5]) > 0:
            #     isFireDetected = True
            #     stop_flight(object)
            #     print("Fire Detected: ", isFireDetected)
        result_img = annotator.result()

        ret, buffer = cv2.imencode('.jpg', result_img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # cv2.imshow('result', result_img)

    cap.release()
