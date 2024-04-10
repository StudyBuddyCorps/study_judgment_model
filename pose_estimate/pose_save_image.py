import os
import cv2
import numpy as np
import mediapipe as mp

# Mediapipe의 Pose 모델을 로드합니다.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 이미지 폴더 경로
image_folder = '/Users/baejuhyeon/Datasets/capstone/study_dataset/phone/images'

# 결과를 저장할 파일 경로
# output_file = 'pose_estimation_results.txt'
output_folder = '../result/pose_estimation_result'

# 필요한 키포인트 목록 정의
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

# 이미지 폴더 아래의 모든 이미지 파일을 순회합니다.
for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        # 이미지 파일 경로
        image_path = os.path.join(image_folder, filename)

        # 이미지를 읽어옵니다.
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 이미지에서 포즈 추정을 수행합니다.
        results = pose.process(image_rgb)

        # 결과를 시각화합니다.
        if results.pose_landmarks is not None:
            key_coords = {}

            # shoulder
            left_shoulder_x = int(
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image.shape[1])
            left_shoulder_y = int(
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image.shape[0])

            right_shoulder_x = int(
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image.shape[1])
            right_shoulder_y = int(
                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image.shape[0])

            # 키포인트 좌표 추출
            for keypoint in keypoints:
                landmark_x = int(results.pose_landmarks.landmark[keypoint].x * image.shape[1])
                landmark_y = int(results.pose_landmarks.landmark[keypoint].y * image.shape[0])
                key_coords[keypoint.name] = (landmark_x, landmark_y)
                cv2.circle(image, (landmark_x, landmark_y), 10, (0, 255, 0), -1)

            height, width, _ = image.shape
            font_scale = min(width, height) / 1000.0  # 글자 크기를 해상도에 맞게 조절
            thickness = max(int(font_scale / 2),4)
            slope = (right_shoulder_y - left_shoulder_y) / (right_shoulder_x - left_shoulder_x)
            cv2.putText(image, f"Slope: {slope:.2f}", (left_shoulder_x, left_shoulder_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness, cv2.LINE_AA)

            cv2.line(image, key_coords["LEFT_SHOULDER"], key_coords["RIGHT_SHOULDER"], (255, 0, 0),2)
            left_hand = np.array([key_coords["LEFT_WRIST"],key_coords["LEFT_PINKY"],key_coords["LEFT_INDEX"]],np.int32)
            right_hand = np.array([key_coords["RIGHT_WRIST"], key_coords["RIGHT_PINKY"], key_coords["RIGHT_INDEX"]],
                                 np.int32)
            cv2.polylines(image, [left_hand], True, (255, 0, 0), thickness)
            cv2.polylines(image, [right_hand],True, (255, 0, 0), thickness)

            output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}_pose_estimation.jpg')
            cv2.imwrite(output_path, image)

            # # 결과를 텍스트 파일에 저장
            # f.write(f"Image: {filename}\n")
            # if results.pose_landmarks is not None:
            #     for landmark in results.pose_landmarks.landmark:
            #         f.write(f"Landmark {landmark.x}, {landmark.y}, {landmark.z}\n")
            # f.write("\n")

# 메모리에서 모델을 해제합니다.
pose.close()
