from ultralytics import YOLO
import cv2 as cv
import os
import cv2 as cv
import mediapipe as mp
import math

from detector.detect import detection_result, is_sleeping
from pose_estimate.pose_return_result import pose_result, return_slope


def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def is_holding_phone(detection_rst=None, key_coords=None, threshold=500):
    if detection_rst[2] is None or key_coords is None:
        return False
    r_x, r_y = key_coords["RIGHT_WRIST"]
    l_x, l_y = key_coords["LEFT_WRIST"]
    x1, y1, x2, y2 = detection_rst[2]

    d1 = (calculate_distance(r_x, r_y, x1, y1) + calculate_distance(r_x, r_y, x2, y2)) / 2
    d2 = (calculate_distance(l_x, l_y, x1, y1) + calculate_distance(l_x, l_y, x2, y2)) / 2
    print(d1, d2)

    return d1 < threshold or d2 < threshold


def write_text(image, text, position, font=cv.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(0, 0, 0), thickness=3):
    """
    :param image: 이미지 (NumPy 배열)
    :param text: 쓸 텍스트
    :param position: 텍스트의 위치 좌표 (tuple 형식)
    :param font: 폰트
    :param font_scale: 폰트 크기 배율
    :param color: 텍스트 색상 (BGR 순서, 기본값은 검은색)
    :param thickness: 텍스트 두께
    :return: 텍스트가 쓰인 이미지
    """
    cv.putText(image, text, position, font, font_scale, color, thickness)
    return image


def initialize_models(pose_threshold=0.5):
    det_model = YOLO("models/train3_best.pt")
    mp_pose = mp.solutions.pose
    pose_model = mp_pose.Pose(static_image_mode=True, min_detection_confidence=pose_threshold)
    key_points = [
        mp_pose.PoseLandmark.LEFT_SHOULDER,
        mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.RIGHT_WRIST,
        mp_pose.PoseLandmark.LEFT_WRIST
    ]
    return det_model, pose_model, key_points


def inference(conf=0.7, slop_threshold=0.3, decision_length=3):
    # 웹캠 연결
    idx = 0
    is_phone_holding_list = [False for _ in range(decision_length)]
    is_in_sleep_list = [False for _ in range(decision_length)]

    cap = cv.VideoCapture(0)
    det_model, pose_model, key_points = initialize_models()

    # 연결 확인
    if not cap.isOpened():
        print("webcam connection failed.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("frame unreadable.")
            break

        detection_rst = detection_result(det_model, frame, conf)
        skeleton_rst = pose_result(pose_model, frame, key_points)

        # is_in_sleep = is_sleeping(detection_rst)
        is_in_sleep_list[idx] = is_sleeping(detection_rst)
        is_in_sleep = False
        if sum(is_in_sleep_list) > decision_length / 2:
            is_in_sleep = True

        slop = return_slope(skeleton_rst)

        # is_phone_holding = is_holding_phone(detection_rst, skeleton_rst)
        is_phone_holding_list[idx] = is_holding_phone(detection_rst, skeleton_rst)
        is_phone_holding = False
        if sum(is_phone_holding_list) > decision_length / 2:
            is_phone_holding = True

        result = write_text(frame, f"is in sleep: {is_in_sleep}", (50, 50))
        result = write_text(result, f"bad posture: {abs(slop) >= slop_threshold}", (50, 100))
        result = write_text(result, f"phone: {is_phone_holding}", (50, 150))

        cv.imshow('Webcam', result)
        idx = (idx + 1) % decision_length

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    inference()
