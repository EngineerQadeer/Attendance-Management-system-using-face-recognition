import tkinter as tk
from tkinter import Message, Text
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
    "success_bg": "#006600",
    "success_fg": "#FFFFFF",
    "error_fg": "#FF0000",
    "clear_bg": "#cc0066",
}

FONTS = {
    "title": ("Verdana", 22, "bold"),
    "label": ("Verdana", 15, "bold"),
    "input": ("Verdana", 20, "bold"),
    "button": ("Verdana", 14, "bold"),
    "notification": ("Verdana", 16, "bold"),
}

ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")
d = {}
index = 0


def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap("AMS.ico")
    sb.title("Manual Attendance Entry")
    sb.geometry("620x380")
    sb.minsize(600, 350)
    sb.configure(background=COLORS["bg"])

    # Configure grid for centering
    sb.grid_columnconfigure(0, weight=1)
    sb.grid_rowconfigure(0, weight=0)
    sb.grid_rowconfigure(1, weight=1)

    def err_screen_for_subject():
        def ec_delete():
            ec.destroy()

        global ec
        ec = tk.Tk()
        ec.geometry("400x120")
        ec.iconbitmap("AMS.ico")
        ec.title("Warning!!")
        ec.configure(background=COLORS["bg"])
        ec.grid_columnconfigure(0, weight=1)

        tk.Label(
            ec,
            text="Please enter subject name!!!",
            fg=COLORS["error_fg"],
            bg=COLORS["bg"],
            font=FONTS["notification"],
        ).grid(row=0, column=0, pady=20)

        tk.Button(
            ec,
            text="OK",
            command=ec_delete,
            fg=COLORS["button_fg"],
            bg=COLORS["button_bg"],
            width=9,
            height=1,
            activebackground="red",
            font=FONTS["button"],
            cursor="hand2",
            bd=3,
        ).grid(row=1, column=0)

    def fill_attendance():
        global subb
        subb = SUB_ENTRY.get()

        if subb == "":
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.iconbitmap("AMS.ico")
            MFW.title("Manual Attendance - " + str(subb))
            MFW.geometry("900x550")
            MFW.minsize(850, 500)
            MFW.configure(background=COLORS["bg"])

            # Configure grid
            MFW.grid_columnconfigure(0, weight=1)
            MFW.grid_rowconfigure(0, weight=0)
            MFW.grid_rowconfigure(1, weight=1)

            # Header
            tk.Label(
                MFW,
                text=f"Manual Attendance - {subb}",
                bg=COLORS["bg"],
                fg=COLORS["heading"],
                font=FONTS["title"],
                pady=15,
            ).grid(row=0, column=0, sticky="ew")

            # Content frame
            content_frame = tk.Frame(MFW, bg=COLORS["bg"])
            content_frame.grid(row=1, column=0, pady=20)

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry("420x120")
                errsc2.iconbitmap("AMS.ico")
                errsc2.title("Warning!!")
                errsc2.configure(background=COLORS["bg"])
                errsc2.grid_columnconfigure(0, weight=1)

                tk.Label(
                    errsc2,
                    text="Please enter Student & Enrollment!!!",
                    fg=COLORS["error_fg"],
                    bg=COLORS["bg"],
                    font=FONTS["notification"],
                ).grid(row=0, column=0, pady=20)

                tk.Button(
                    errsc2,
                    text="OK",
                    command=del_errsc2,
                    fg=COLORS["button_fg"],
                    bg=COLORS["button_bg"],
                    width=9,
                    height=1,
                    activebackground="red",
                    font=FONTS["button"],
                    cursor="hand2",
                    bd=3,
                ).grid(row=1, column=0)

            def testVal(inStr, acttyp):
                if acttyp == "1":  # insert
                    if not inStr.isdigit():
                        return False
                return True

            # Enrollment input row
            tk.Label(
                content_frame,
                text="Enter Enrollment",
                width=16,
                height=2,
                fg=COLORS["primary_text"],
                bg=COLORS["input_bg"],
                font=FONTS["label"],
                relief=tk.RIDGE,
                bd=3,
            ).grid(row=0, column=0, padx=10, pady=10)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(
                content_frame,
                width=22,
                validate="key",
                bg=COLORS["input_bg"],
                fg=COLORS["input_text"],
                insertbackground="white",
                font=FONTS["input"],
                bd=3,
                relief=tk.RIDGE,
            )
            ENR_ENTRY["validatecommand"] = (ENR_ENTRY.register(testVal), "%P", "%d")
            ENR_ENTRY.grid(row=0, column=1, padx=10, pady=10)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            tk.Button(
                content_frame,
                text="Clear",
                command=remove_enr,
                fg=COLORS["button_fg"],
                bg=COLORS["clear_bg"],
                width=10,
                height=1,
                activebackground="red",
                font=FONTS["button"],
                cursor="hand2",
                bd=3,
            ).grid(row=0, column=2, padx=10)

            # Student name input row
            tk.Label(
                content_frame,
                text="Enter Student Name",
                width=16,
                height=2,
                fg=COLORS["primary_text"],
                bg=COLORS["input_bg"],
                font=FONTS["label"],
                relief=tk.RIDGE,
                bd=3,
            ).grid(row=1, column=0, padx=10, pady=10)

            STUDENT_ENTRY = tk.Entry(
                content_frame,
                width=22,
                bg=COLORS["input_bg"],
                fg=COLORS["input_text"],
                insertbackground="white",
                font=FONTS["input"],
                bd=3,
                relief=tk.RIDGE,
            )
            STUDENT_ENTRY.grid(row=1, column=1, padx=10, pady=10)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            tk.Button(
                content_frame,
                text="Clear",
                command=remove_student,
                fg=COLORS["button_fg"],
                bg=COLORS["clear_bg"],
                width=10,
                height=1,
                activebackground="red",
                font=FONTS["button"],
                cursor="hand2",
                bd=3,
            ).grid(row=1, column=2, padx=10)

            def enter_data_DB():
                global index
                global d
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == "":
                    err_screen1()
                elif STUDENT == "":
                    err_screen1()
                else:
                    if index == 0:
                        d = {index: {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}}
                        index += 1
                        ENR_ENTRY.delete(0, "end")
                        STUDENT_ENTRY.delete(0, "end")
                    else:
                        d[index] = {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                        index += 1
                        ENR_ENTRY.delete(0, "end")
                        STUDENT_ENTRY.delete(0, "end")
                print(d)

            def create_csv():
                if not d:
                    Notifi.configure(
                        text="No data to save!",
                        bg=COLORS["bg"],
                        fg=COLORS["error_fg"],
                    )
                    Notifi.grid(row=3, column=0, columnspan=3, pady=15)
                    return
                    
                df = pd.DataFrame(d)
                # Ensure directory exists
                if not os.path.exists("Attendance(Manually)"):
                    os.makedirs("Attendance(Manually)")
                    
                csv_name = (
                    "Attendance(Manually)/"
                    + subb
                    + "_"
                    + Date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                df.to_csv(csv_name)
                Notifi.configure(
                    text="CSV Created Successfully!",
                    bg=COLORS["success_bg"],
                    fg=COLORS["success_fg"],
                    width=35,
                    height=2,
                    font=FONTS["notification"],
                )
                Notifi.grid(row=3, column=0, columnspan=3, pady=15)

            # Notification label
            Notifi = tk.Label(
                content_frame,
                text="",
                bg=COLORS["bg"],
                fg=COLORS["heading"],
                width=35,
                height=2,
                font=FONTS["notification"],
            )

            # Button row
            button_frame = tk.Frame(content_frame, bg=COLORS["bg"])
            button_frame.grid(row=2, column=0, columnspan=3, pady=25)

            tk.Button(
                button_frame,
                text="Enter Data",
                command=enter_data_DB,
                fg=COLORS["button_fg"],
                bg=COLORS["button_bg"],
                width=14,
                height=2,
                activebackground=COLORS["input_bg"],
                font=FONTS["button"],
                cursor="hand2",
                bd=5,
            ).pack(side=tk.LEFT, padx=15)

            tk.Button(
                button_frame,
                text="Convert to CSV",
                command=create_csv,
                fg=COLORS["button_fg"],
                bg=COLORS["button_bg"],
                width=14,
                height=2,
                activebackground=COLORS["input_bg"],
                font=FONTS["button"],
                cursor="hand2",
                bd=5,
            ).pack(side=tk.LEFT, padx=15)

            def attf():
                if os.path.exists("Attendance(Manually)"):
                    os.startfile("Attendance(Manually)")

            tk.Button(
                button_frame,
                text="Check Sheets",
                command=attf,
                fg=COLORS["button_fg"],
                bg=COLORS["button_bg"],
                width=14,
                height=2,
                activebackground=COLORS["input_bg"],
                font=FONTS["button"],
                cursor="hand2",
                bd=5,
            ).pack(side=tk.LEFT, padx=15)

            MFW.mainloop()

    # Header
    header_frame = tk.Frame(sb, bg=COLORS["bg"], relief=tk.RIDGE, bd=5)
    header_frame.grid(row=0, column=0, sticky="ew")
    header_frame.grid_columnconfigure(0, weight=1)

    tk.Label(
        header_frame,
        text="Manual Attendance Entry",
        bg=COLORS["bg"],
        fg=COLORS["heading"],
        font=FONTS["title"],
        pady=10,
    ).grid(row=0, column=0)

    # Content frame
    content_frame = tk.Frame(sb, bg=COLORS["bg"])
    content_frame.grid(row=1, column=0, pady=30)

    # Subject input
    tk.Label(
        content_frame,
        text="Enter Subject",
        width=14,
        height=2,
        fg=COLORS["primary_text"],
        bg=COLORS["input_bg"],
        font=FONTS["label"],
        relief=tk.RIDGE,
        bd=5,
    ).grid(row=0, column=0, padx=10, pady=10)

    global SUB_ENTRY
    SUB_ENTRY = tk.Entry(
        content_frame,
        width=20,
        bg=COLORS["input_bg"],
        fg=COLORS["input_text"],
        insertbackground="white",
        font=FONTS["input"],
        bd=5,
        relief=tk.RIDGE,
    )
    SUB_ENTRY.grid(row=0, column=1, padx=10, pady=10)

    # Button
    tk.Button(
        content_frame,
        text="Fill Attendance",
        command=fill_attendance,
        fg=COLORS["button_fg"],
        bg=COLORS["button_bg"],
        width=18,
        height=2,
        activebackground=COLORS["input_bg"],
        font=FONTS["button"],
        cursor="hand2",
        bd=5,
    ).grid(row=1, column=0, columnspan=2, pady=20)

    sb.mainloop()
