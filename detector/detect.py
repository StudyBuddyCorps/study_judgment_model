from ultralytics import YOLO
import cv2 as cv
import os

# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("../models/train3_best.pt")  # load a pretrained model (recommended for training)

'''
source can be (folder_path, image_path, webcam(0)
folder_path = " "
image_path = " "
save (save images)
save_txt (save as labels)
'''

image_path = "/Users/baejuhyeon/Desktop/sleep_63_pose_estimation.jpg"

results = model.predict(source=image_path, save=True, show=True, conf=0.3)  # save predictions as labels
# path = model.export(format="onnx")  # export the model to ONNX format
