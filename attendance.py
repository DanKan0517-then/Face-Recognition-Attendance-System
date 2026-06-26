# attendance.py
# -----------------------------------------
# Face Recognition Attendance System
# Raspberry Pi 3B
# Python 3.5
# OpenCV 3.3.1
# -----------------------------------------

import cv2
import os
import csv
from datetime import datetime

# -----------------------------------------
# Load Haar Cascade
# -----------------------------------------

cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"

face_detector = cv2.CascadeClassifier(cascade_path)

if face_detector.empty():
    print("Error: Haar Cascade not loaded.")
    exit()

# -----------------------------------------
# Files
# -----------------------------------------

dataset_path = "dataset"
attendance_file = "attendance.csv"

# -----------------------------------------
# Load Dataset
# -----------------------------------------

def load_faces():

    database = {}

    if not os.path.exists(dataset_path):
        return database

    for person in os.listdir(dataset_path):

        person_folder = os.path.join(dataset_path, person)

        if not os.path.isdir(person_folder):
            continue

        images = []

        for image_name in os.listdir(person_folder):

            image_path = os.path.join(person_folder, image_name)

            img = cv2.imread(
                image_path,
                cv2.IMREAD_GRAYSCALE
            )

            if img is not None:

                img = cv2.resize(img, (100, 100))

                images.append(img)

        database[person] = images

    return database

# -----------------------------------------
# Face Recognition
# -----------------------------------------

def recognize_face(face, database):

    best_match = "Unknown"
    lowest_score = float("inf")

    for person in database:

        for stored_face in database[person]:

            diff = cv2.absdiff(face, stored_face)

            score = diff.sum()

            if score < lowest_score:

                lowest_score = score
                best_match = person

    THRESHOLD = 400000

    if lowest_score < THRESHOLD:
        return best_match

    return "Unknown"

# -----------------------------------------
# Attendance
# -----------------------------------------

def mark_attendance(name):

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    already_present = False

    if os.path.exists(attendance_file):

        with open(attendance_file, "r") as file:

            reader = csv.reader(file)

            for row in reader:

                if len(row) >= 2:

                    if row[0] == name and row[1] == today:

                        already_present = True
                        break

    if not already_present:

        with open(attendance_file, "a") as file:

            writer = csv.writer(file)

            writer.writerow([
                name,
                today,
                current_time,
                "Present"
            ])

        print("{} marked present".format(name))

# -----------------------------------------
# Main
# -----------------------------------------

database = load_faces()

print("Loaded {} users".format(len(database)))

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Cannot open camera.")
    exit()

while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(80, 80)
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        face = cv2.resize(face, (100, 100))

        name = recognize_face(face, database)

        if name != "Unknown":
            mark_attendance(name)

        color = (0, 255, 0)

        if name == "Unknown":
            color = (0, 0, 255)

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            color,
            2
        )

        cv2.putText(
            frame,
            name,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow("Attendance System", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

# -----------------------------------------
# Cleanup
# -----------------------------------------

camera.release()
cv2.destroyAllWindows()
