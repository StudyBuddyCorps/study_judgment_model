import cv2
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
cap = cv2.VideoCapture(0)


def get_eye_points(landmarks, eye_points):
    return [landmarks.part(point) for point in eye_points]


def draw_eye_contour(frame, eye_points, color=(0, 255, 0), thickness=2):
    for i in range(len(eye_points)):
        cv2.line(frame, (eye_points[i].x, eye_points[i].y),
                 (eye_points[(i + 1) % len(eye_points)].x, eye_points[(i + 1) % len(eye_points)].y), color, thickness)


while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        left_eye_points = get_eye_points(landmarks, [36, 37, 38, 39, 40, 41])
        right_eye_points = get_eye_points(landmarks, [42, 43, 44, 45, 46, 47])

        draw_eye_contour(frame, left_eye_points)
        draw_eye_contour(frame, right_eye_points)

    cv2.imshow("Eye Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()