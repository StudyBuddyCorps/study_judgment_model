import os
import json

# 디렉토리와 하위 디렉토리 설정
base_path = '/Users/baejuhyeon/Datasets/capstone/study_dataset'
folders = ['phone', 'sleep', 'study']
subfolders = ['labels']

# 결과를 저장할 딕셔너리 초기화
results = []

# 각 폴더 순회
for folder in folders:
    for subfolder in subfolders:
        label_dir = os.path.join(base_path, folder, subfolder)
        print(label_dir)
        # labels 폴더가 존재하는 경우에만 처리
        if os.path.exists(label_dir):
            # labels 폴더 내의 모든 텍스트 파일 순회
            for filename in os.listdir(label_dir):
                if filename.endswith(".txt"):
                    file_path = os.path.join(label_dir, filename)
                    # 텍스트 파일 열기
                    with open(file_path, 'r') as file:
                        # 첫 번째 숫자를 읽어와서 리스트에 추가
                        lines = file.readlines()
                        first_numbers = [int(line.split()[0]) for line in lines]
                        # 결과 딕셔너리에 추가
                        result_entry = {
                            'id': os.path.splitext(filename)[0],
                            'class': first_numbers
                        }
                        results.append(result_entry)


sum_list = [sum(1 for result in results if idx in result['class']) for idx in range(5)]
index = {0: "awake_face", 1: "awake_person", 2: "phone", 3: "sleeping_face", 4: "sleeping_person"}
[print(num, index[idx]) for num, idx in zip(sum_list,index)]

# 결과를 JSON 파일로 저장
json_file_path = '../result/labels.json'

with open(json_file_path, 'w') as json_file:
    json.dump(results, json_file)

print("Results saved to", json_file_path)
