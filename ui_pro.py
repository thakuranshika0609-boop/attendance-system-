import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import time
import random

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("500x600")
root.configure(bg="#0f0c29")

# ---------------- CANVAS BACKGROUND ----------------
canvas = tk.Canvas(root, bg="#0f0c29", highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

# ---------------- GLITCH BACKGROUND ----------------
def glitch_bg():
    canvas.delete("glitch")

    # scan lines
    for i in range(0, 600, 8):
        if random.random() < 0.15:
            canvas.create_line(
                0, i, 500, i,
                fill=random.choice(["#00f5ff", "#ff4ecd", "#c77dff"]),
                width=1,
                tags="glitch"
            )

    # glitch blocks
    if random.random() < 0.3:
        x = random.randint(0, 450)
        y = random.randint(0, 550)
        w = random.randint(20, 80)
        h = random.randint(2, 6)

        canvas.create_rectangle(
            x, y, x+w, y+h,
            fill=random.choice(["#00f5ff", "#ff4ecd", "#c77dff"]),
            outline="",
            tags="glitch"
        )

    root.after(120, glitch_bg)

glitch_bg()

# ---------------- MAIN FRAME ----------------
frame = tk.Frame(root, bg="#1a1a2e")
frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=520)

# ---------------- TITLE ----------------
title = tk.Label(frame,
                 text="FACE ATTENDANCE SYSTEM",
                 font=("Consolas", 18, "bold"),
                 fg="#c77dff",
                 bg="#1a1a2e")
title.pack(pady=20)

# ---------------- CLOCK ----------------
clock_label = tk.Label(frame,
                       font=("Consolas", 12),
                       fg="#00f5ff",
                       bg="#1a1a2e")
clock_label.pack()

def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text="TIME : " + current_time)   # ✅ FIXED
    root.after(1000, update_clock)

update_clock()

# ---------------- INPUT ----------------
name_var = tk.StringVar()

entry = tk.Entry(frame,
                 textvariable=name_var,
                 font=("Consolas", 13),
                 bg="#0f0c29",
                 fg="white",
                 insertbackground="white",
                 justify="center",
                 bd=1,
                 relief="flat")
entry.insert(0, "Enter Name")
entry.pack(pady=20, ipady=8, ipadx=10)

# ---------------- FUNCTIONS ----------------
def register_user():
    name = name_var.get()

    if name == "" or name == "Enter Name":
        messagebox.showwarning("Warning", "Enter valid name")
        return

    subprocess.run([sys.executable, "register.py", name])


def mark_attendance():
    subprocess.run([sys.executable, "final_attendance.py"])


def open_dashboard():
    subprocess.run([sys.executable, "dashboard.py"])


def exit_app():
    root.destroy()

# ---------------- BUTTON STYLE ----------------
def create_btn(text, cmd, color):
    btn = tk.Button(frame,
                    text=text,
                    command=cmd,
                    font=("Consolas", 12, "bold"),
                    bg="#1a1a2e",
                    fg=color,
                    activebackground="#2a2a40",
                    activeforeground="white",
                    bd=2,
                    relief="solid",
                    width=22,
                    height=2,
                    highlightthickness=2,
                    highlightbackground=color,
                    highlightcolor=color,
                    cursor="hand2")

    # hover effect
    def on_enter(e):
        btn.config(bg="#2a2a40", fg="white")

    def on_leave(e):
        btn.config(bg="#1a1a2e", fg=color)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn

# ---------------- BUTTONS ----------------
create_btn("Register User", register_user, "#ff4ecd").pack(pady=10)
create_btn("Mark Attendance", mark_attendance, "#00f5ff").pack(pady=10)
create_btn("Dashboard", open_dashboard, "#c77dff").pack(pady=10)
create_btn("Exit", exit_app, "#ff6b6b").pack(pady=10)

# ---------------- FOOTER ----------------
footer = tk.Label(frame,
                  text="SYSTEM READY",
                  font=("Consolas", 10),
                  fg="#888",
                  bg="#1a1a2e")
footer.pack(side="bottom", pady=10)

# ---------------- RUN ----------------
root.mainloop()