import cv2 as cv
import mediapipe as mp


def pose_result(pose=None, image=None, key_points=None):
    results = pose.process(image)

    # 결과를 시각화합니다.
    if results.pose_landmarks is not None:
        key_coords = {}

        for keypoint in key_points:
            landmark_x = int(results.pose_landmarks.landmark[keypoint].x * image.shape[1])
            landmark_y = int(results.pose_landmarks.landmark[keypoint].y * image.shape[0])
            key_coords[keypoint.name] = (landmark_x, landmark_y)

        return key_coords
    else:
        return None


def return_slope(key_coords=None):
    if key_coords is None:
        return 0.0
    slope = (key_coords["RIGHT_SHOULDER"][1] - key_coords["LEFT_SHOULDER"][1]) / (
            key_coords["RIGHT_SHOULDER"][0] - key_coords["LEFT_SHOULDER"][0])
    return slope


def return_hand(key_coords=None):
    left_hand = key_coords["LEFT_WRIST"]
    right_hand = key_coords["LEFT_WRIST"]

    return left_hand, right_hand
