# Face Attendance System

A desktop application for marking attendance using face detection with OpenCV and a custom Tkinter UI.

## Features
- Face registration via webcam
- Real-time attendance marking
- CSV-based logging (date, lecture, time, status)
- Dashboard with weekly stats and graphs
- Styled UI with neon/glitch effects

## Tech Stack
- Python
- OpenCV
- Tkinter
- Pandas
- Matplotlib

## How to Run
```bash
pip install opencv-python pandas matplotlib
python ui_pro.py
Project Structure
ui_pro.py            # Main UI
register.py          # Capture & save faces
final_attendance.py  # Mark attendance
dashboard.py         # Reports & graphs
attendance.csv       # Data file (auto-created)
Notes
Ensure webcam access is enabled
Delete attendance.csv if schema changes
