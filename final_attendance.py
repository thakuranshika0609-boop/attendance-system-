import cv2
import os
import csv
from datetime import datetime

# ---------------- LECTURE TIME ----------------
def get_current_lecture():
    now = datetime.now().strftime("%H:%M")

    if "10:00" <= now < "10:45":
        return "Lecture 1"
    elif "10:45" <= now < "11:30":
        return "Lecture 2"
    elif "11:30" <= now < "12:15":
        return "Lecture 3"
    elif "12:15" <= now < "13:00":
        return "Lecture 4"
    elif "13:30" <= now < "14:15":
        return "Lecture 5"
    elif "14:15" <= now < "15:00":
        return "Lecture 6"
    elif "15:00" <= now < "15:45":
        return "Lecture 7"
    else:
        return None

# ---------------- STATUS LOGIC ----------------
def get_status(lecture):
    now = datetime.now().strftime("%H:%M")

    timings = {
        "Lecture 1": ("10:00","10:05","10:15"),
        "Lecture 2": ("10:45","10:50","11:00"),
        "Lecture 3": ("11:30","11:35","11:45"),
        "Lecture 4": ("12:15","12:20","12:30"),
        "Lecture 5": ("13:30","13:35","13:45"),
        "Lecture 6": ("14:15","14:20","14:30"),
        "Lecture 7": ("15:00","15:05","15:15"),
    }

    start, ontime_end, late_end = timings.get(lecture, ("00:00","00:00","00:00"))

    if start <= now < ontime_end:
        return "On Time"
    elif ontime_end <= now < late_end:
        return "Late"
    else:
        return "Absent"

# ---------------- FACE ----------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

dataset_path = "dataset"

known_names = [
    os.path.splitext(f)[0]
    for f in os.listdir(dataset_path)
    if f.endswith(".jpg")
]

# ---------------- CSV ----------------
file_name = "attendance.csv"

if not os.path.exists(file_name):
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Lecture", "Time", "Status"])

marked_today = set()

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    lecture = get_current_lecture()

    # ❌ NO LECTURE TIME
    if lecture is None:
        cv2.putText(frame, "Attendance Closed",
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) == 27:
            break
        continue

    face_index = 0

    for (x, y, w, h) in faces:

        if known_names:
            name = known_names[face_index % len(known_names)]
            face_index += 1
        else:
            name = "Unknown"

        status = get_status(lecture)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.putText(frame, f"{name} ({lecture})", (x, y-25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.putText(frame, status, (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2)

        today = datetime.now().strftime("%Y-%m-%d")

        if (name, today, lecture) not in marked_today:
            time = datetime.now().strftime("%H:%M:%S")

            with open(file_name, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, today, lecture, time, status])

            print("Marked:", name, lecture, status)
            marked_today.add((name, today, lecture))

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()