from flask import Flask, render_template, Response
import cv2 as cv
import numpy as np

import sys
sys.path.append("/Users/baejuhyeon/Developer/PycharmProjects/study_judgment_model")

from detector.detect import detection_result, is_sleeping
from pose_estimate.pose_return_result import pose_result, return_slope
from demo import initialize_models, is_holding_phone, write_text, draw_result_on_image

app = Flask(__name__)

det_model, pose_model, key_points = initialize_models()


@app.route('/')
def index():
    # 메인 페이지 렌더링
    return render_template('index.html')


def generate():
    cap = cv.VideoCapture(0)
    decision_length = 3
    idx = 0
    is_phone_holding_list = [False for _ in range(decision_length)]
    is_in_sleep_list = [False for _ in range(decision_length)]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detection_rst = detection_result(det_model, frame, 0.7)
        skeleton_rst = pose_result(pose_model, frame, key_points)

        # 졸음 여부 판단
        is_in_sleep_list[idx] = is_sleeping(detection_rst)
        is_in_sleep = sum(is_in_sleep_list) > decision_length / 2

        # 자세 기울기 계산
        slop = return_slope(skeleton_rst)

        # 핸드폰 소지 여부 판단
        is_phone_holding_list[idx] = is_holding_phone(detection_rst, skeleton_rst)
        is_phone_holding = sum(is_phone_holding_list) > decision_length / 2

        result = frame.copy()
        result = write_text(result, f"is in sleep: {is_in_sleep}", (50, 50), boolean=is_in_sleep)
        result = write_text(result, f"bad posture: {abs(slop) >= 0.3}", (50, 100), boolean=abs(slop) >= 0.3)
        result = write_text(result, f"phone: {is_phone_holding}", (50, 150), boolean=is_phone_holding)

        drw_result = frame.copy()
        drw_result = draw_result_on_image(drw_result, detection_rst, skeleton_rst)
        # result = np.hstack((result, drw_result))

        # convert frame to JPEG for streaming
        _, buffer = cv.imencode('.jpg', result)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        idx = (idx + 1) % decision_length

    cap.release()


@app.route('/video_feed')
def video_feed():
    # return video stream
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000)
