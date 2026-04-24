import cv2
import os
import sys

# Create folder
if not os.path.exists("dataset"):
    os.makedirs("dataset")

# 🔥 TAKE NAME FROM UI (NOT TERMINAL)
if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    print("No name provided from UI")
    exit()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera not opening")
    exit()

print("Press 'S' to capture OR 'Q' to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1)

    # S press
    if key == ord('s') or key == ord('S'):
        path = f"dataset/{name}.jpg"
        cv2.imwrite(path, frame)

        print(f"✅ Saved at: {path}")
        break

    # Q press
    if key == ord('q') or key == ord('Q'):
        break

cap.release()
cv2.destroyAllWindows()