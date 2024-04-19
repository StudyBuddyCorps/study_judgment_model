import os


def is_single_line(file_path):
    try:
        with open(file_path, 'r') as file:
            line_count = sum(1 for line in file)
            return line_count == 1
    except Exception as e:
        print(f"An error occurred while checking file: {file_path}")
        print(e)
        return False


def process_file(file_path):
    with open(file_path, 'r') as file:
        new_lines = ""
        lines = file.readlines()  # 파일의 첫 줄을 읽어옴
        for line in lines:
            parts = line.rstrip().split(" ")  # 공백으로 분리
            if len(parts) != 5:
                # 한 줄에 정확히 5개의 요소가 아니라면 처리하지 않음
                return

            # 맨 앞의 정수가 0이면 1로 변경
            if parts[0] == '0':
                parts[0] = '3'
            elif parts[0] == '1':
                parts[0] = '4'
            # 변경된 줄을 다시 문자열로 조합
            new_lines += (" ".join(parts)+'\n')
            # 변경된 내용을 파일에 쓰기
        with open(file_path, 'w') as file:
            file.write(new_lines)


def process_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if "txt" in file_path:
            if os.path.isfile(file_path):
                # 파일인 경우에만 처리
                process_file(file_path)


# 주어진 폴더 내의 모든 파일 처리
folder_path = '/Users/baejuhyeon/Documents/capstone/study_dataset/sleep_change/texts/'
process_files_in_directory(folder_path)