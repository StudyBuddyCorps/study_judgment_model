from ultralytics import YOLO

model = YOLO('models/yolov8n.pt ')

model.train(data='coco.yaml', epochs=50)
metrics = model.val()  # evaluate model performance on the validation set
# path = model.export(format="onnx")  # export the model to ONNX format
