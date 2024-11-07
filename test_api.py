import requests
import time

image_path = "/Users/baejuhyeon/Developer/PycharmProjects/study_judgment_model/result/pose_estimation_result/sleep_183_pose_estimation.jpg"

# url = "http://3.107.8.184:5000/upload_image"

url = "http://192.168.1.120:5001/upload_image"


with open(image_path, 'rb') as img_file:
    files = {'file': img_file}

    start_time = time.time()

    response = requests.post(url, files=files, verify=False)

if response.status_code == 200:
    result = response.json()
    print("판독 결과:")
    print(f"잠을 자고 있는가: {result['is_sleeping']}")
    print(f"나쁜 자세인가: {result['bad_posture']}")
    print(f"휴대폰을 들고 있는가: {result['is_holding_phone']}")
else:
    print(f"Error: {response.status_code}, {response.text}")

# End the timer and calculate elapsed time
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")
