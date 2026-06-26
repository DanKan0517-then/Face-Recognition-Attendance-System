# Face Recognition Attendance System - Yanshee / Raspberry Pi 3B

Complete implementation guide for a face-recognition attendance system using Raspberry Pi 3B, Python 3.5 and OpenCV 3.3.1 without cv2.face.

Recognize known faces using the camera and mark attendance automatically once per day for approximately 10 people.

## 1. Project Overview

The Face Recognition Attendance System is a lightweight computer vision application developed for the Yanshee Robot using Raspberry Pi 3B.

The system automatically detects faces from a live camera feed, recognizes registered users by comparing captured face images with stored grayscale images, and records attendance only once per day.

Since OpenCV 3.3.1 on Raspberry Pi does not include the `cv2.face` module, the project uses a simple image comparison method (`cv2.absdiff`) instead of LBPH or deep learning models.

---

## 2. Full Pipeline

Camera Feed

↓

Face Detection (Haar Cascade)

↓

Crop Face

↓

Resize Face (100 × 100)

↓

Compare With Stored Faces

↓

Recognize Person

↓

Check Attendance for Today

↓

Save Attendance to CSV

---

## 3. Environment Details

**Hardware**

Raspberry Pi 3B

USB Camera / Pi Camera

Yanshee Robot

**Software**

Python Version: 3.5.3

OpenCV Version: 3.3.1

**Limitation**

cv2.face module unavailable (LBPH cannot be used)

---

## 4. Commands Used

Check Python version

```bash
python3
```

Check OpenCV version

```python
import cv2
print(cv2.__version__)
```

Check cv2.face module

```python
print(hasattr(cv2, "face"))
```

Find Haar Cascade

```bash
find /usr -name "haarcascade_frontalface_default.xml"
```

Run face collection

```bash
python3 collect_faces.py
```

Run attendance system

```bash
python3 attendance.py
```

---

## 5. Folder Structure

```text
attendance/
│
├── dataset/
│     ├── Danushk/
│     ├── Rahul/
│     ├── Priya/
│
├── attendance.csv
├── collect_faces.py
├── attendance.py
└── README.md
```

---

## 6. collect_faces.py

Purpose

Collect face samples for every user.

Workflow

• Ask user for name

• Create dataset folder

• Open webcam

• Detect face using Haar Cascade

• Crop detected face

• Resize face to 100 × 100

• Save 30 grayscale face images

• Store images inside dataset/person_name

---

## 7. attendance.py

Purpose

Recognize registered users and automatically mark attendance.

Workflow

• Load stored face images

• Open camera

• Detect faces using Haar Cascade

• Crop and resize detected face

• Compare with stored images using cv2.absdiff()

• Find closest matching person

• Check attendance.csv

• Mark attendance once per day

• Save Name, Date, Time and Status

---

## 8. Attendance Output

Example attendance.csv

```text
Danushk,2026-05-21,09:22:15,Present
Rahul,2026-05-21,09:25:40,Present
Priya,2026-05-21,09:28:01,Present
```

---

## 9. Recognition Method

Since OpenCV's cv2.face module is unavailable, the project uses image difference comparison.

Recognition Steps

• Convert image to grayscale

• Crop face

• Resize to 100 × 100

• Compare with every stored image using cv2.absdiff()

• Calculate pixel difference score

• Lowest score becomes the recognized user

• If score exceeds threshold, display Unknown

---

## 10. Common Error

Error

```text
(-215) !empty() in function detectMultiScale
```

Cause

Cascade classifier not loaded.

Fix

```text
/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml
```

---

## 11. Final Working Flow

First run **collect_faces.py** for every user.

This creates the dataset by storing 30 face images for each registered person.

Then run **attendance.py**.

The camera continuously detects faces, compares them with the stored dataset, recognizes known users, checks whether attendance has already been marked for the current day, and if not, stores the attendance record inside **attendance.csv**.

Attendance is recorded only once per day for each registered user.

---

## 12. Future Improvements

• Face Embedding based Recognition

• InsightFace Integration

• FaceNet Support

• MySQL Database

• Web Dashboard

• Anti-Spoofing

• Multi-Camera Support

• Cloud Attendance System

• Email Notifications

---

## 13. Conclusion

The Face Recognition Attendance System provides a simple and efficient attendance solution for Raspberry Pi 3B without requiring OpenCV's `cv2.face` module. By combining Haar Cascade face detection with grayscale image comparison, the system is capable of recognizing registered users and automatically maintaining daily attendance records while remaining lightweight enough to run on low-resource hardware such as the Yanshee Robot.
