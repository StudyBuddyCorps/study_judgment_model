from ultralytics import YOLO

model = YOLO('../models/train3_best.pt')

model.train(data='coco.yaml', epochs=50)
metrics = model.val()  # evaluate model performance on the validation set
