import os
from collections import defaultdict

# 기본 경로 설정
path_to_folder = "/Users/baejuhyeon/Datasets/capstone/study_dataset/split_dataset"
base_dirs = ['test', 'train', 'val']
labels_folder = 'labels'

# 클래스 개수를 저장할 딕셔너리 초기화
class_counts = defaultdict(int)

# 모든 디렉토리를 순회하며 클래스 개수를 셈
for base_dir in base_dirs:
    labels_path = os.path.join(path_to_folder, base_dir, labels_folder)

    # labels 폴더 안의 모든 파일을 읽음
    for filename in os.listdir(labels_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(labels_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    class_id = int(line.split()[0])  # 첫 번째 값이 클래스 ID
                    class_counts[class_id] += 1

# 결과 출력
for class_id, count in sorted(class_counts.items()):
    print(f'Class {class_id}: {count} instances')