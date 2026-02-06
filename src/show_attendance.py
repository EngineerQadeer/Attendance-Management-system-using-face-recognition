import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

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


def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = "Please enter the subject name."
            text_to_speech(t)
            return

        try:
            filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
            if not filenames:
                t = f"No attendance records found for {Subject}"
                text_to_speech(t)
                # Show error in notification
                error_label.configure(
                    text=f"❌ No records found for '{Subject}'",
                    fg="#FF0000",
                )
                error_label.grid(row=2, column=0, columnspan=2, pady=10)
                return
                
            df = [pd.read_csv(f) for f in filenames]
            newdf = df[0]
            for i in range(1, len(df)):
                newdf = newdf.merge(df[i], how="outer")
            newdf.fillna(0, inplace=True)
            newdf["Attendance"] = 0
            for i in range(len(newdf)):
                newdf["Attendance"].iloc[i] = (
                    str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + "%"
                )
            newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

            # Show styled attendance table
            show_attendance_table(Subject, newdf)
            print(newdf)
        except Exception as e:
            print(f"Error: {e}")
            t = "Error calculating attendance"
            text_to_speech(t)
            error_label.configure(
                text=f"❌ Error: {str(e)[:50]}",
                fg="#FF0000",
            )
            error_label.grid(row=2, column=0, columnspan=2, pady=10)

    def show_attendance_table(Subject, attendance_df):
        """Display attendance in a styled, scrollable table."""
        root = tk.Toplevel(subject)
        root.title("Attendance Report - " + Subject)
        root.geometry("800x550")
        root.minsize(700, 450)
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
            text=f"📊 Attendance Report - {Subject}",
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
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Read and display CSV
        cs = f"Attendance\\{Subject}\\attendance.csv"
        try:
            with open(cs) as file:
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
                            width=14,
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
                text=f"\n✅ Total Students: {record_count}",
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
    subject.title("View Attendance")
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
        text="📊 View Attendance Report",
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
        text="📋 View Attendance",
        command=calculate_attendance,
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
    
    # Error/status label (hidden initially)
    error_label = tk.Label(
        content_frame,
        text="",
        bg=COLORS["bg"],
        fg=COLORS["heading"],
        font=FONTS["label"],
    )

    subject.mainloop()
