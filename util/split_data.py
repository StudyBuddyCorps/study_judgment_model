import os
import random
import shutil

# 폴더 경로 설정
base_folder = "/Users/baejuhyeon/Documents/capstone/study_dataset"
output_folder = "/Users/baejuhyeon/Documents/capstone/study_dataset/split_dataset"
categories = ["phone", "sleep_change", "study"]

# 결과를 저장할 폴더 생성
os.makedirs(output_folder, exist_ok=True)

# 각 카테고리마다 작업 수행
for category in categories:
    image_folder = os.path.join(base_folder, category, "images")
    label_folder = os.path.join(base_folder, category, "labels")

    # 이미지와 라벨 파일 이름 리스트 가져오기
    images = os.listdir(image_folder)
    labels = os.listdir(label_folder)

    # 파일 이름을 랜덤하게 섞음
    random.shuffle(images)

    # 데이터셋을 7:2:1 비율로 분할
    num_images = len(images)
    num_train = int(num_images * 0.7)
    num_val = int(num_images * 0.2)
    num_test = num_images - num_train - num_val

    # 분할된 데이터셋을 저장할 폴더 생성
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(output_folder, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_folder, split, "labels"), exist_ok=True)

    # 데이터셋을 분할하여 저장
    for i, image in enumerate(images):
        if i < num_train:
            split = "train"
        elif i < num_train + num_val:
            split = "val"
        else:
            split = "test"

        label = image.replace("jpg","txt")

        # 이미지 파일과 라벨 파일을 목적지 폴더로 복사
        shutil.copy(os.path.join(image_folder, image), os.path.join(output_folder, split, "images", image))
        shutil.copy(os.path.join(label_folder, label), os.path.join(output_folder, split, "labels", label))

        print(f"Moved {image} and {label} to {split}/{category}")

print("Dataset splitting completed.")