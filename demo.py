import time
import cv2
import dlib
from scipy.spatial import distance



EYE_AR_THRESH = 0.26
EYE_AR_CONSEC_FRAMES = 10



def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear_aspect_ratio = (A+B)/(2.0*C)
    return ear_aspect_ratio


def drowsy_detect():
    cap = cv2.VideoCapture(0)
    hog_face_detector = dlib.get_frontal_face_detector()
    dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    EAR = 0
    counter = 0
    counter2 = 0

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = hog_face_detector(gray)
        for face in faces:
            face_landmarks = dlib_facelandmark(gray, face)
            leftEye = []
            rightEye = []

            for n in range(36,42):
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                leftEye.append((x,y))
                next_point = n+1
                if n == 41:
                    next_point = 36
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                # cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

            for n in range(42,48):
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                rightEye.append((x,y))
                next_point = n+1
                if n == 47:
                    next_point = 42
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                # cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

            left_ear = calculate_EAR(leftEye)
            right_ear = calculate_EAR(rightEye)


            # EAR-Eye Aspect Ratio
            EAR = (left_ear+right_ear)/2
            EAR = round(EAR,2)

            if EAR<0.26:
                cv2.putText(frame,"Blinked",(20,100), cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4)
                print("Blinked")
                pass
            # print(EAR)

        if EAR < EYE_AR_THRESH:
            counter += 1
        else:
            counter = 0

        if counter >= EYE_AR_CONSEC_FRAMES:
            cv2.putText(frame, "Drowsy", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)
            print("abnormal")
            print("Counter2 =", counter2)
            counter2 += 1
            counter = 0

            if counter2 == 6:
                counter2 =0
                for i in range(10):
                    print("Triggered")
                    time.sleep(0.05)

        else:
            pass
            # print("normal condition")

        cv2.imshow("camera", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    drowsy_detect()