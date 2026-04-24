import pandas as pd
import matplotlib.pyplot as plt

# ---------------- LOAD CSV ----------------
try:
    df = pd.read_csv("attendance.csv")
except:
    print("❌ No attendance data found!")
    exit()

# ---------------- REQUIRED COLUMNS ----------------
required_cols = ["Name", "Date", "Lecture", "Time", "Status"]

# If old CSV → stop safely
for col in required_cols:
    if col not in df.columns:
        print("❌ Old CSV format detected!")
        print("👉 Please delete attendance.csv and run attendance again.")
        exit()

# ---------------- CLEAN DATA ----------------
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
df = df.dropna(subset=["Date"])

# ---------------- LAST 7 DAYS ----------------
last_week = df[df["Date"] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]

if last_week.empty:
    print("❌ No data for last 7 days")
    exit()

# ---------------- WEEKLY STATUS ----------------
weekly = last_week.groupby(["Name", "Status"]).size().unstack(fill_value=0)

print("\n===== WEEKLY STATUS REPORT =====\n")
print(weekly)

# ---------------- TOTAL ATTENDANCE ----------------
total_attendance = last_week.groupby("Name").size()

print("\n===== TOTAL ATTENDANCE =====\n")
print(total_attendance)

# ---------------- GRAPH 1 ----------------
weekly.plot(kind="bar", figsize=(10,6))
plt.title("Weekly Attendance (Status)")
plt.xlabel("Students")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------- GRAPH 2 ----------------
total_attendance.plot(kind="bar", color="purple", figsize=(8,5))
plt.title("Total Weekly Attendance")
plt.xlabel("Students")
plt.ylabel("Total")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------------- INDIVIDUAL REPORT ----------------
name = input("\nEnter student name: ")

person = last_week[last_week["Name"] == name]

if not person.empty:
    report = person["Status"].value_counts()

    print(f"\n===== {name} REPORT =====\n")
    print(report)

    # Pie chart
    report.plot(kind="pie", autopct="%1.1f%%")
    plt.title(f"{name} Attendance")
    plt.ylabel("")
    plt.show()

    # Percentage
    total = len(person)
    present = report.get("On Time", 0) + report.get("Late", 0)

    percentage = (present / total) * 100
    print(f"{name} Attendance %: {percentage:.2f}%")

else:
    print("❌ No data found for this student")