# collect_faces.py
# ----------------------------
# Collect 30 face images for one person
# Raspberry Pi 3B
# Python 3.5
# OpenCV 3.3.1
# ----------------------------

import cv2
import os

# ----------------------------
# Enter Person Name
# ----------------------------

name = input("Enter name: ").strip()

dataset_path = "dataset"
person_folder = os.path.join(dataset_path, name)

if not os.path.exists(person_folder):
    os.makedirs(person_folder)

# ----------------------------
# Load Haar Cascade
# ----------------------------

cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"

face_detector = cv2.CascadeClassifier(cascade_path)

if face_detector.empty():
    print("Error: Haar Cascade not loaded.")
    exit()

# ----------------------------
# Open Camera
# ----------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Cannot open camera.")
    exit()

print("\nCollecting face images...")
print("Look at the camera.")
print("Press ESC to stop.\n")

count = 0

# ----------------------------
# Capture Loop
# ----------------------------

while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(80, 80)
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        face = cv2.resize(face, (100, 100))

        count += 1

        filename = os.path.join(
            person_folder,
            "{}.jpg".format(count)
        )

        cv2.imwrite(filename, face)

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Images: {}".format(count),
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Collection", frame)

    key = cv2.waitKey(1) & 0xFF

    # ESC Key
    if key == 27:
        break

    # Stop after collecting 30 images
    if count >= 30:
        break

# ----------------------------
# Cleanup
# ----------------------------

camera.release()
cv2.destroyAllWindows()

print("\nFace collection completed.")
print("Person :", name)
print("Images :", count)
print("Saved to:", person_folder)
