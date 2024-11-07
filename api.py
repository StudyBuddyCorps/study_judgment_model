from flask import Flask, jsonify, request
import cv2 as cv
import numpy as np
import sys
from PIL import Image
import io
import dlib
import time

# Importing custom functions
sys.path.append("/Users/baejuhyeon/Developer/PycharmProjects/study_judgment_model")
from detector.detect import detection_result, is_sleeping
from pose_estimate.pose_return_result import pose_result, return_slope
from demo import initialize_models, is_holding_phone
from eye_track.detect_eye_blink import detect_eyes, calculate_ear_binocular

app = Flask(__name__)

# Initialize models
det_model, pose_model, key_points = initialize_models()
hog_face_detector = dlib.get_frontal_face_detector()
dlib_face_landmark = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

EAR_THRESHOLD = 0.2
close_count = 0
last_save = 0


def check_sleeping_status(frame):
    global close_count, last_save

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = hog_face_detector(gray)

    if not faces:
        return "blinking", close_count, last_save

    for face in faces:
        face_landmarks = dlib_face_landmark(gray, face)
        left_eye, right_eye = detect_eyes(face_landmarks)
        EAR = calculate_ear_binocular(left_eye, right_eye)

        if EAR < EAR_THRESHOLD:
            close_count += 1
            time.sleep(0.05)

            if time.time() - last_save > 5:
                last_save = time.time()
                close_count = 0

            if close_count > 10:
                return "sleeping", close_count, last_save
            else:
                return "blinking", close_count, last_save

    close_count = 0
    return "blinking", close_count, last_save


# Route to process image upload and return result
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read image
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    in_memory_file.seek(0)
    img = Image.open(in_memory_file)
    img = np.array(img)
    # Pre-process the image (convert from RGB to BGR)
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

    cv.imwrite('output_image.jpg', img)

    # Perform detection and pose estimation
    detection_rst = detection_result(det_model, img, 0.7)
    skeleton_rst = pose_result(pose_model, img, key_points)

    # Determine if the person is sleeping, has bad posture, or is holding a phone
    status, close_count, last_save = check_sleeping_status(img)
    is_in_sleep = (is_sleeping(detection_rst) or (status == "sleeping"))
    slop = return_slope(skeleton_rst)
    is_phone_holding = is_holding_phone(detection_rst, skeleton_rst)

    import pdb; pdb.set_trace()

    # Return results as JSON
    return jsonify({
        "is_sleeping": is_in_sleep,
        "bad_posture": abs(slop) >= 0.3,
        "is_holding_phone": is_phone_holding
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True)
