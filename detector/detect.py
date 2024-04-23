from ultralytics import YOLO
import numpy as np
import cv2 as cv
import os

'''
0: awake_face
1: awake_person
2: phone
3: sleeping_face
4: sleeping_person
'''


def detection_result(det_model, img, conf):
    detection_rst = [None, None, None, None, None]
    results = det_model.predict(save=False, stream=True, verbose=False, show=True,source=0, conf=0.3)

    for r in results:
        for i in range(len(r.boxes.cls)):
            if r.boxes.conf[i] >= conf:
                detection_rst[int(r.boxes.cls[i])] = np.array(r.boxes.xyxy[i])

    return detection_rst


def is_sleeping(detection_rst=None):
    is_in_sleep = (detection_rst[3] is not None) or (detection_rst[4] is not None)
    return is_in_sleep


if __name__ == "__main__":
    '''
    source can be (folder_path, image_path, webcam(0)
    folder_path = " "
    image_path = " "
    save (save images)
    save_txt (save as labels)
    '''
    model = YOLO("../models/train3_best.pt")  # load a pretrained model (recommended for training)
    image_path = "/Users/baejuhyeon/Datasets/capstone/study_dataset/phone/images/phone_1.jpg"
    returns = detection_result(model, image_path, 0.5)
    print(returns)
