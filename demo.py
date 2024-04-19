from ultralytics import YOLO
import cv2 as cv
import os
import cv2 as cv
import mediapipe as mp

from detector.detect import detection_result, is_sleeping
from pose_estimate.pose_return_result import pose_result, return_slope


def is_holding_phone(detection_rst=None, pose_rst=None):
    return detection_rst[2] is not None


def write_text(image, text, position, font=cv.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(0, 0, 0), thickness=3):
    """
    :param image: 이미지 (NumPy 배열)
    :param text: 쓸 텍스트
    :param position: 텍스트의 위치 좌표 (tuple 형식)
    :param font: 폰트
    :param font_scale: 폰트 크기 배율
    :param color: 텍스트 색상 (BGR 순서, 기본값은 흰색)
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


def inference(conf=0.7, slop_threshold=0.3):
    # 웹캠 연결
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

        is_in_sleep = is_sleeping(detection_rst)
        slop = return_slope(skeleton_rst)
        is_phone_holding = is_holding_phone(detection_rst)

        result = write_text(frame, f"is in sleep: {is_in_sleep}", (50, 50))
        result = write_text(result, f"bad posture: {abs(slop)>=slop_threshold}", (50, 100))
        result = write_text(result, f"phone: {is_phone_holding}", (50, 150))

        cv.imshow('Webcam', result)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    inference()
