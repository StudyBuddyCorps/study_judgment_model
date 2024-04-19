import os
import cv2
import numpy as np
import mediapipe as mp

from pose_return_result import pose_result, return_slope

# Load Mediapipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

image_folder = '/Users/baejuhyeon/Datasets/capstone/study_dataset/phone/images'
output_folder = '../result/pose_estimation_result'

# Key points to detect
keypoints = [
    mp_pose.PoseLandmark.LEFT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_SHOULDER,
    mp_pose.PoseLandmark.RIGHT_THUMB,
    mp_pose.PoseLandmark.LEFT_THUMB,
    mp_pose.PoseLandmark.RIGHT_INDEX,
    mp_pose.PoseLandmark.LEFT_INDEX,
    mp_pose.PoseLandmark.RIGHT_PINKY,
    mp_pose.PoseLandmark.LEFT_PINKY,
    mp_pose.PoseLandmark.RIGHT_WRIST,
    mp_pose.PoseLandmark.LEFT_WRIST
]

for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):

        image_path = os.path.join(image_folder, filename)

        # read image
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        key_coords = pose_result(image_rgb, pose, keypoints)

        if key_coords is not None:
            left_hand = np.array([key_coords["LEFT_WRIST"], key_coords["LEFT_PINKY"], key_coords["LEFT_INDEX"]],
                                 np.int32)
            right_hand = np.array([key_coords["RIGHT_WRIST"], key_coords["RIGHT_PINKY"], key_coords["RIGHT_INDEX"]],
                                  np.int32)

            slope = return_slope(key_coords)

            height, width, _ = image.shape
            font_scale = min(width, height) / 1000.0  # match font scale to image resolution
            thickness = max(int(font_scale / 2), 4)

            cv2.line(image, key_coords["LEFT_SHOULDER"], key_coords["RIGHT_SHOULDER"], (255, 0, 0), 2)
            cv2.polylines(image, [left_hand], True, (255, 0, 0), thickness)
            cv2.polylines(image, [right_hand], True, (255, 0, 0), thickness)

            cv2.putText(image, f"Slope: {slope:.2f}", 10 , 10, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness, cv2.LINE_AA)

            # write to image
            output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_pose_estimation.jpg')
            cv2.imwrite(output_path, image)

            # save result to txt
            # f.write(f"Image: {filename}\n")
            # if results.pose_landmarks is not None:
            #     for landmark in results.pose_landmarks.landmark:
            #         f.write(f"Landmark {landmark.x}, {landmark.y}, {landmark.z}\n")
            # f.write("\n")

pose.close()
