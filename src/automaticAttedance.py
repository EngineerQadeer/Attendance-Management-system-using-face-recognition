import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

# ============== DESIGN SYSTEM ==============
COLORS = {
    "bg": "#1c1c1c",
    "primary_text": "#FFFF00",
    "heading": "#00ff00",
    "input_bg": "#333333",
    "input_text": "#FFFFFF",
    "button_bg": "#000000",
    "button_fg": "#FFFF00",
    "header_bg": "#333333",
    "header_fg": "#00ff00",
    "data_fg": "#FFFFFF",
}

FONTS = {
    "title": ("Verdana", 25, "bold"),
    "label": ("Verdana", 15, "bold"),
    "input": ("Verdana", 20, "bold"),
    "button": ("Verdana", 14, "bold"),
    "table": ("Verdana", 12, "bold"),
}

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel\\Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails\\studentdetails.csv"
attendance_path = "Attendance"


def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train model"
                    Notifica.configure(
                        text=e,
                        bg=COLORS["bg"],
                        fg=COLORS["primary_text"],
                        width=33,
                        font=FONTS["label"],
                    )
                    Notifica.grid(row=4, column=0, columnspan=2, pady=10)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font_cv = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id
                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font_cv, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font_cv, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                print(aa)
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                full_path = os.path.join(path, fileName)
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv(full_path, index=False)

                m = "Attendance Filled Successfully for " + Subject
                Notifica.configure(
                    text=m,
                    bg=COLORS["bg"],
                    fg=COLORS["heading"],
                    width=40,
                    relief=RIDGE,
                    bd=3,
                    font=FONTS["label"],
                )
                text_to_speech(m)
                Notifica.grid(row=4, column=0, columnspan=2, pady=10)

                cam.release()
                cv2.destroyAllWindows()

                # Show attendance result in styled window
                show_attendance_table(full_path, Subject, attendance)
                print(attendance)
            except Exception as ex:
                print(f"Error: {ex}")
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    def show_attendance_table(file_path, Subject, attendance_df):
        """Display attendance in a styled, scrollable table."""
        root = tk.Toplevel(subject)
        root.title("Attendance of " + Subject)
        root.geometry("700x450")
        root.minsize(600, 400)
        root.configure(background=COLORS["bg"])
        root.iconbitmap("AMS.ico")
        
        # Configure grid for expansion
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=0)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=0)
        
        # Header with title
        header_frame = tk.Frame(root, bg=COLORS["bg"], relief=RIDGE, bd=5)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            header_frame,
            text=f"📋 Attendance Record - {Subject}",
            bg=COLORS["bg"],
            fg=COLORS["heading"],
            font=FONTS["title"],
            pady=15,
        ).grid(row=0, column=0)
        
        # Scrollable frame container
        container = tk.Frame(root, bg=COLORS["bg"])
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        # Canvas and scrollbars
        canvas = tk.Canvas(container, bg=COLORS["bg"], highlightthickness=0)
        v_scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Read CSV and display data
        try:
            with open(file_path, newline="") as file:
                reader = csv.reader(file)
                r = 0
                for col in reader:
                    c = 0
                    for row in col:
                        # Header row styling
                        if r == 0:
                            bg_color = COLORS["header_bg"]
                            fg_color = COLORS["header_fg"]
                        else:
                            bg_color = COLORS["bg"]
                            fg_color = COLORS["data_fg"]
                        
                        label = tk.Label(
                            scrollable_frame,
                            width=18,
                            height=2,
                            fg=fg_color,
                            font=FONTS["table"],
                            bg=bg_color,
                            text=row,
                            relief=tk.RIDGE,
                            bd=2,
                        )
                        label.grid(row=r, column=c, padx=2, pady=2)
                        c += 1
                    r += 1
                    
            # Show record count
            record_count = r - 1  # Subtract header row
            tk.Label(
                scrollable_frame,
                text=f"\n✅ Total Records: {record_count}",
                bg=COLORS["bg"],
                fg=COLORS["primary_text"],
                font=FONTS["label"],
            ).grid(row=r+1, column=0, columnspan=3, pady=10, sticky="w")
            
        except Exception as ex:
            tk.Label(
                scrollable_frame,
                text=f"Error loading data: {ex}",
                bg=COLORS["bg"],
                fg="#FF0000",
                font=FONTS["label"],
            ).grid(row=0, column=0, pady=20)
        
        # Footer with close button
        footer_frame = tk.Frame(root, bg=COLORS["bg"])
        footer_frame.grid(row=2, column=0, pady=15)
        
        tk.Button(
            footer_frame,
            text="Close",
            command=root.destroy,
            bd=5,
            font=FONTS["button"],
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            height=1,
            width=12,
            cursor="hand2",
            activebackground=COLORS["input_bg"],
        ).pack()
        
        # Bind mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                os.startfile(f"Attendance\\{sub}")
            except:
                t = f"No folder found for {sub}"
                text_to_speech(t)

    # ============== MAIN WINDOW ==============
    subject = Tk()
    subject.title("Take Attendance")
    subject.geometry("650x420")
    subject.minsize(620, 380)
    subject.resizable(True, True)
    subject.configure(background=COLORS["bg"])
    subject.iconbitmap("AMS.ico")
    
    # Configure grid for centering
    subject.grid_columnconfigure(0, weight=1)
    subject.grid_rowconfigure(0, weight=0)
    subject.grid_rowconfigure(1, weight=1)
    
    # Header
    header_frame = tk.Frame(subject, bg=COLORS["bg"], relief=RIDGE, bd=5)
    header_frame.grid(row=0, column=0, sticky="ew")
    header_frame.grid_columnconfigure(0, weight=1)
    
    tk.Label(
        header_frame,
        text="📷 Take Attendance",
        bg=COLORS["bg"],
        fg=COLORS["heading"],
        font=FONTS["title"],
        pady=15,
    ).grid(row=0, column=0)
    
    # Content frame
    content_frame = tk.Frame(subject, bg=COLORS["bg"])
    content_frame.grid(row=1, column=0, pady=20)
    
    # Subject input
    tk.Label(
        content_frame,
        text="Enter Subject",
        width=14,
        height=2,
        bg=COLORS["input_bg"],
        fg=COLORS["primary_text"],
        bd=5,
        relief=RIDGE,
        font=FONTS["label"],
    ).grid(row=0, column=0, padx=10, pady=15)
    
    tx = tk.Entry(
        content_frame,
        width=18,
        bd=5,
        bg=COLORS["input_bg"],
        fg=COLORS["input_text"],
        insertbackground="white",
        relief=RIDGE,
        font=FONTS["input"],
    )
    tx.grid(row=0, column=1, padx=10, pady=15)
    
    # Button frame
    button_frame = tk.Frame(content_frame, bg=COLORS["bg"])
    button_frame.grid(row=1, column=0, columnspan=2, pady=25)
    
    tk.Button(
        button_frame,
        text="📸 Fill Attendance",
        command=FillAttendance,
        bd=5,
        font=FONTS["button"],
        bg=COLORS["button_bg"],
        fg=COLORS["button_fg"],
        height=2,
        width=16,
        relief=RIDGE,
        cursor="hand2",
        activebackground=COLORS["input_bg"],
    ).pack(side=LEFT, padx=15)
    
    tk.Button(
        button_frame,
        text="📂 Check Sheets",
        command=Attf,
        bd=5,
        font=FONTS["button"],
        bg=COLORS["button_bg"],
        fg=COLORS["button_fg"],
        height=2,
        width=16,
        relief=RIDGE,
        cursor="hand2",
        activebackground=COLORS["input_bg"],
    ).pack(side=LEFT, padx=15)
    
    # Notification label (hidden initially)
    Notifica = tk.Label(
        content_frame,
        text="",
        bg=COLORS["bg"],
        fg=COLORS["heading"],
        width=40,
        height=2,
        font=FONTS["label"],
    )
    
    subject.mainloop()
