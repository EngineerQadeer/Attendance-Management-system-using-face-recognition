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
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# ============== DESIGN SYSTEM ==============
COLORS = {
    "bg": "#1c1c1c",           # Deep Charcoal background
    "primary_text": "#FFFF00", # Yellow text
    "heading": "#00ff00",      # Green headings
    "input_bg": "#333333",     # Dark grey inputs
    "input_text": "#FFFFFF",   # White input text
    "button_bg": "#000000",    # Black buttons
    "button_fg": "#FFFF00",    # Yellow button text
    "exit_bg": "#FF0000",      # Red exit button
    "exit_fg": "#FFFFFF",      # White exit text
}

FONTS = {
    "title": ("Verdana", 27, "bold"),
    "subtitle": ("Verdana", 25, "bold"),
    "button": ("Verdana", 14, "bold"),
    "label": ("Verdana", 14),
    "input": ("Verdana", 18, "bold"),
    "message": ("Verdana", 14, "bold"),
}


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "/TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"


# ============== MAIN WINDOW SETUP ==============
window = Tk()
window.title("Smart Attendance System")
window.geometry("1280x720")
window.minsize(900, 700)
window.configure(background=COLORS["bg"])

# Configure grid weights for centering
window.grid_rowconfigure(0, weight=0)  # Header row
window.grid_rowconfigure(1, weight=0)  # Title row
window.grid_rowconfigure(2, weight=1)  # Action area (expandable)
window.grid_rowconfigure(3, weight=0)  # Footer row
window.grid_columnconfigure(0, weight=1)


# ============== HELPER FUNCTIONS ==============
def del_sc1():
    sc1.destroy()


def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("450x130")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background=COLORS["bg"])
    sc1.resizable(0, 0)
    
    # Center the content
    sc1.grid_columnconfigure(0, weight=1)
    
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg=COLORS["primary_text"],
        bg=COLORS["bg"],
        font=("Verdana", 16, "bold"),
    ).grid(row=0, column=0, pady=15)
    
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg=COLORS["primary_text"],
        bg=COLORS["input_bg"],
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 14, "bold"),
        cursor="hand2",
        bd=3,
    ).grid(row=1, column=0, pady=10)


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


# ============== HEADER SECTION ==============
header_frame = tk.Frame(window, bg=COLORS["bg"], relief=RIDGE, bd=10)
header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=0)
header_frame.grid_columnconfigure(2, weight=1)

# Logo and Title in header
logo = Image.open("UI_Image/0001.png")
logo = logo.resize((50, 47), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)

# Center container for logo and title
center_header = tk.Frame(header_frame, bg=COLORS["bg"])
center_header.grid(row=0, column=1)

logo_label = tk.Label(center_header, image=logo1, bg=COLORS["bg"])
logo_label.pack(side=LEFT, padx=5)

title_label = tk.Label(
    center_header,
    text="Smart Attendance System",
    bg=COLORS["bg"],
    fg=COLORS["primary_text"],
    font=FONTS["title"],
)
title_label.pack(side=LEFT, padx=5)


# ============== SUBTITLE SECTION ==============
subtitle_label = tk.Label(
    window,
    text="Welcome to the Face Recognition Based Attendance System",
    bg=COLORS["bg"],
    fg=COLORS["primary_text"],
    bd=10,
    font=FONTS["subtitle"],
)
subtitle_label.grid(row=1, column=0, pady=10)


# ============== ACTION AREA ==============
action_frame = tk.Frame(window, bg=COLORS["bg"])
action_frame.grid(row=2, column=0, sticky="nsew", padx=50, pady=20)

# Configure 3 equal columns for buttons
action_frame.grid_columnconfigure(0, weight=1)
action_frame.grid_columnconfigure(1, weight=1)
action_frame.grid_columnconfigure(2, weight=1)
action_frame.grid_rowconfigure(0, weight=1)
action_frame.grid_rowconfigure(1, weight=0)
action_frame.grid_rowconfigure(2, weight=1)


def create_action_block(parent, icon_path, button_text, command, col):
    """Create a styled action block with icon and button."""
    block_frame = tk.Frame(parent, bg=COLORS["bg"])
    block_frame.grid(row=1, column=col, padx=20)
    
    # Icon
    icon_img = Image.open(icon_path)
    icon_img = icon_img.resize((120, 120), Image.LANCZOS)
    icon = ImageTk.PhotoImage(icon_img)
    
    icon_label = tk.Label(block_frame, image=icon, bg=COLORS["bg"], cursor="hand2")
    icon_label.image = icon  # Keep reference
    icon_label.pack(pady=(0, 20))
    icon_label.bind("<Button-1>", lambda e: command())
    
    # Button
    btn = tk.Button(
        block_frame,
        text=button_text,
        command=command,
        bd=5,
        font=FONTS["button"],
        bg=COLORS["button_bg"],
        fg=COLORS["button_fg"],
        height=2,
        width=20,
        cursor="hand2",
        activebackground=COLORS["input_bg"],
        activeforeground=COLORS["primary_text"],
    )
    btn.pack()
    
    return block_frame


# ============== REGISTER WINDOW ==============
def TakeImageUI():
    ImageUI = Toplevel(window)
    ImageUI.title("Register New Student")
    ImageUI.geometry("850x550")
    ImageUI.minsize(800, 500)
    ImageUI.configure(background=COLORS["bg"])
    ImageUI.iconbitmap("AMS.ico")
    
    # Configure grid for centering
    ImageUI.grid_columnconfigure(0, weight=1)
    ImageUI.grid_rowconfigure(0, weight=0)
    ImageUI.grid_rowconfigure(1, weight=1)
    
    # Header
    header = tk.Label(
        ImageUI,
        text="Register Your Face",
        bg=COLORS["bg"],
        fg=COLORS["heading"],
        font=FONTS["title"],
        pady=15,
    )
    header.grid(row=0, column=0, sticky="ew")
    
    # Main content frame
    content_frame = tk.Frame(ImageUI, bg=COLORS["bg"])
    content_frame.grid(row=1, column=0, pady=20)
    
    # Sub-heading
    tk.Label(
        content_frame,
        text="Enter the details",
        bg=COLORS["bg"],
        fg=COLORS["primary_text"],
        font=("Verdana", 20, "bold"),
    ).grid(row=0, column=0, columnspan=2, pady=(0, 30))
    
    # Enrollment Number
    tk.Label(
        content_frame,
        text="Enrollment No",
        width=14,
        height=2,
        bg=COLORS["input_bg"],
        fg=COLORS["primary_text"],
        bd=5,
        relief=RIDGE,
        font=FONTS["label"],
    ).grid(row=1, column=0, padx=10, pady=10)
    
    txt1 = tk.Entry(
        content_frame,
        width=20,
        bd=5,
        validate="key",
        bg=COLORS["input_bg"],
        fg=COLORS["input_text"],
        insertbackground="white",
        relief=RIDGE,
        font=FONTS["input"],
    )
    txt1.grid(row=1, column=1, padx=10, pady=10)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")
    
    # Name
    tk.Label(
        content_frame,
        text="Name",
        width=14,
        height=2,
        bg=COLORS["input_bg"],
        fg=COLORS["primary_text"],
        bd=5,
        relief=RIDGE,
        font=FONTS["label"],
    ).grid(row=2, column=0, padx=10, pady=10)
    
    txt2 = tk.Entry(
        content_frame,
        width=20,
        bd=5,
        bg=COLORS["input_bg"],
        fg=COLORS["input_text"],
        insertbackground="white",
        relief=RIDGE,
        font=FONTS["input"],
    )
    txt2.grid(row=2, column=1, padx=10, pady=10)
    
    # Notification
    tk.Label(
        content_frame,
        text="Notification",
        width=14,
        height=2,
        bg=COLORS["input_bg"],
        fg=COLORS["primary_text"],
        bd=5,
        relief=RIDGE,
        font=FONTS["label"],
    ).grid(row=3, column=0, padx=10, pady=10)
    
    message = tk.Label(
        content_frame,
        text="",
        width=28,
        height=2,
        bd=5,
        bg=COLORS["input_bg"],
        fg=COLORS["heading"],
        relief=RIDGE,
        font=FONTS["message"],
    )
    message.grid(row=3, column=1, padx=10, pady=10)
    
    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")
    
    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )
    
    # Button frame
    button_frame = tk.Frame(content_frame, bg=COLORS["bg"])
    button_frame.grid(row=4, column=0, columnspan=2, pady=30)
    
    tk.Button(
        button_frame,
        text="Take Image",
        command=take_image,
        bd=5,
        font=FONTS["button"],
        bg=COLORS["button_bg"],
        fg=COLORS["button_fg"],
        height=2,
        width=14,
        cursor="hand2",
        activebackground=COLORS["input_bg"],
    ).pack(side=LEFT, padx=15)
    
    tk.Button(
        button_frame,
        text="Train Image",
        command=train_image,
        bd=5,
        font=FONTS["button"],
        bg=COLORS["button_bg"],
        fg=COLORS["button_fg"],
        height=2,
        width=14,
        cursor="hand2",
        activebackground=COLORS["input_bg"],
    ).pack(side=LEFT, padx=15)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


# Create action blocks
register_block = create_action_block(
    action_frame, "UI_Image/register.png", "Register a New Student", TakeImageUI, 0
)
attendance_block = create_action_block(
    action_frame, "UI_Image/verifyy.png", "Take Attendance", automatic_attedance, 1
)
view_block = create_action_block(
    action_frame, "UI_Image/attendance.png", "View Attendance", view_attendance, 2
)


# ============== FOOTER SECTION ==============
footer_frame = tk.Frame(window, bg=COLORS["bg"])
footer_frame.grid(row=3, column=0, pady=20)

exit_btn = tk.Button(
    footer_frame,
    text="EXIT",
    bd=5,
    command=quit,
    font=FONTS["button"],
    bg=COLORS["exit_bg"],
    fg=COLORS["exit_fg"],
    height=2,
    width=20,
    cursor="hand2",
    activebackground="#cc0000",
    activeforeground="white",
)
exit_btn.pack()


# ============== MAIN LOOP ==============
window.mainloop()
