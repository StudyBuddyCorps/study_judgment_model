import cv2 as cv
import dlib
from scipy.spatial import distance
import time

EAR_THRESHOLD = 0.2


def calculate_ear(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])

    ear_aspect_ratio = (A + B) / (2.0 * C)
    return ear_aspect_ratio


def calculate_ear_binocular(left_eye, right_eye):
    left_ear = calculate_ear(left_eye)
    right_ear = calculate_ear(right_eye)

    EAR = (left_ear + right_ear) / 2
    EAR = round(EAR, 2)
    return EAR


def detect_eye_landmarks(face_landmarks, start, end):
    eye = []
    for n in range(start, end + 1):
        x = face_landmarks.part(n).x
        y = face_landmarks.part(n).y
        eye.append((x, y))
    return eye


def detect_eyes(face_landmarks):
    left_eye = detect_eye_landmarks(face_landmarks, 36, 41)
    right_eye = detect_eye_landmarks(face_landmarks, 42, 47)

    return left_eye, right_eye


def draw_eye_lines(frame, eye, start, end):
    for i in range(start, end):
        cv.line(frame, eye[i], eye[i+1], (0, 255, 0), 1)
        cv.putText(frame, str(i), eye[i], cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv.LINE_AA)
    cv.line(frame, eye[end], eye[start], (0, 255, 0), 1)
    cv.putText(frame, str(end), eye[end], cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv.LINE_AA)


def check_sleeping_status(frame, hog_face_detector, dlib_face_landmark, close_count, last_save):
    """
    프레임에서 얼굴을 감지하고 EAR을 계산하여 사용자가 sleeping 상태인지 blinking 상태인지 반환합니다.

    Parameters:
        frame (numpy.ndarray): 현재 프레임
        hog_face_detector (dlib.fhog_object_detector): HOG 얼굴 탐지기 모델
        dlib_face_landmark (dlib.shape_predictor): 얼굴 랜드마크 모델
        close_count (int): 눈을 감은 상태를 유지하는 프레임 수
        last_save (float): 마지막으로 상태를 초기화한 시간

    Returns:
        tuple: (status, close_count, last_save)
               status는 'sleeping' 또는 'blinking' 문자열로 상태를 나타냅니다.
               close_count는 갱신된 close_count 값입니다.
               last_save는 갱신된 last_save 값입니다.
    """
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = hog_face_detector(gray)

    # 얼굴이 감지되지 않은 경우 'blinking' 상태로 반환
    if not faces:
        return "blinking", close_count, last_save

    for face in faces:
        # 얼굴 랜드마크 추출
        face_landmarks = dlib_face_landmark(gray, face)

        # 양쪽 눈 좌표 추출
        left_eye, right_eye = detect_eyes(face_landmarks)

        # 양쪽 눈 EAR 계산
        EAR = calculate_ear_binocular(left_eye, right_eye)

        # EAR 기준으로 눈이 감긴 상태인지 판단
        if EAR < EAR_THRESHOLD:
            close_count += 1
            time.sleep(0.05)

            # 5초 이상 경과했으면 close_count 초기화
            if time.time() - last_save > 5:
                last_save = time.time()
                close_count = 0

            # 눈 감은 상태가 10 프레임 이상 지속되면 'sleeping' 반환
            if close_count > 10:
                return "sleeping", close_count, last_save
            else:
                return "blinking", close_count, last_save

    # 눈을 감지 않은 상태라면 close_count 초기화 후 'blinking' 반환
    close_count = 0
    return "blinking", close_count, last_save


def main():
    cap = cv.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    # dlib 인식 모델 정의
    hog_face_detector = dlib.get_frontal_face_detector()
    dlib_face_landmark = dlib.shape_predictor("../models/shape_predictor_68_face_landmarks.dat")


    close_count = 0
    last_save = 0

    while True:
        _, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        faces = hog_face_detector(gray)
        for face in faces:
            face_landmarks = dlib_face_landmark(gray, face)
            left_eye, right_eye = detect_eyes(face_landmarks)

            draw_eye_lines(frame, left_eye, 0, 5)
            draw_eye_lines(frame, right_eye, 0, 5)

            EAR = calculate_ear_binocular(left_eye, right_eye)

            if EAR < EAR_THRESHOLD:
                close_count += 1
                time.sleep(0.05)
                if time.time() - last_save > 5:
                    last_save = time.time()
                    close_count = 0
                if close_count > 10:
                    cv.putText(frame, "Sleeping", (20, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)
                else:
                    cv.putText(frame, "blink", (20, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)

        cv.imshow("Are you Sleepy", frame)

        key = cv.waitKey(30)
        if key == 27:
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
