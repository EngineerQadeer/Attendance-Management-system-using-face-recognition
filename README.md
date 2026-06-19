# 🎓 Smart Attendance System

A modern Face Recognition-based Attendance Management System built with Python and Tkinter. Features a sleek dark mode interface with automated face detection and recognition capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Face Registration** | Capture and store student faces with enrollment details |
| 📸 **Automatic Attendance** | Real-time face recognition to mark attendance |
| 📊 **Attendance Reports** | View and export attendance records by subject |
| 🌙 **Dark Mode UI** | Modern, professional dark theme interface |
| 🔊 **Voice Feedback** | Text-to-speech notifications for user actions |
| 📱 **Responsive Layout** | Grid-based UI that adapts to window resizing |

---

## 🖥️ Screenshots

### Main Dashboard
> Modern dark theme with centered action buttons and icons

### Take Attendance
> Real-time face detection with visual feedback

### Attendance Report
> Scrollable table with styled headers showing attendance records

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam for face capture

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/EngineerQadeer/Attendance-Management-system-using-face-recognition.git
   cd Attendance-Management-system-using-face-recognition
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python attendance.py
   ```

---

## 📦 Dependencies

```
opencv-contrib-python
numpy
pandas
Pillow
pyttsx3
```

---

## 📖 Usage

### 1. Register a New Student
1. Click **"Register a New Student"** on the main dashboard
2. Enter **Enrollment Number** (numeric only)
3. Enter **Student Name**
4. Click **"Take Image"** - Face will be captured (50 samples)
5. Click **"Train Image"** to train the recognition model

### 2. Take Attendance
1. Click **"Take Attendance"** on the main dashboard
2. Enter the **Subject Name**
3. Click **"Fill Attendance"** - Camera will capture faces for 20 seconds
4. Recognized students are automatically marked present
5. Attendance CSV is saved with timestamp

### 3. View Attendance
1. Click **"View Attendance"** on the main dashboard
2. Enter the **Subject Name**
3. Click **"View Attendance"** to see the aggregated report
4. Use **"Check Sheets"** to open the attendance folder

---

## 📁 Project Structure

```
📁 Attendance-Management-system-using-face-recognition/
│
├── 📄 attendance.py              # Main dashboard & entry point
├── 📄 automaticAttedance.py      # Face recognition attendance
├── 📄 show_attendance.py         # View attendance reports
├── 📄 takeImage.py               # Capture student face images
├── 📄 trainImage.py              # Train face recognition model
├── 📄 takemanually.py            # Manual attendance entry
│
├── 📄 haarcascade_frontalface_default.xml  # Face detection model
├── 📄 requirements.txt           # Python dependencies
├── 📄 AMS.ico                    # Application icon
│
├── 📁 Attendance/                # Attendance CSV records
│   └── 📁 [Subject]/             # Per-subject folders
│
├── 📁 StudentDetails/            # Student enrollment data
│   └── 📄 studentdetails.csv
│
├── 📁 TrainingImageLabel/        # Trained face model
│   └── 📄 Trainner.yml
│
└── 📁 UI_Image/                  # UI icons and images
    ├── 📄 register.png
    ├── 📄 attendance.png
    └── 📄 verifyy.png
```

---

## 🎨 UI Design System

The application uses a consistent dark theme:

| Element | Color |
|---------|-------|
| Background | `#1c1c1c` (Deep Charcoal) |
| Primary Text | `#FFFF00` (Yellow) |
| Headings | `#00ff00` (Green) |
| Input Fields | `#333333` (Dark Grey) |
| Buttons | `#000000` (Black) |
| Exit Button | `#FF0000` (Red) |

---

## 🛠️ Technologies Used

- **Python 3** - Core programming language
- **Tkinter** - GUI framework
- **OpenCV** - Face detection and recognition
- **LBPH Algorithm** - Local Binary Pattern Histogram for face recognition
- **Pandas** - Data manipulation and CSV handling
- **pyttsx3** - Text-to-speech engine
- **Pillow** - Image processing

---

## ⚠️ Known Issues

- Attendance calculation may show pandas warnings (cosmetic only, does not affect functionality)
- Requires good lighting for accurate face recognition

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Abdul Qadeer**

---

<p align="center">
  Made with ❤️ using Python
</p>
