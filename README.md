# PreCrash AI — Driver Monitoring Prototype

A Python-based computer vision prototype for driver monitoring, focused on detecting signs of drowsiness using facial landmarks and eye analysis.

## Features

- Real-time webcam monitoring
- Facial landmark detection using MediaPipe
- Eye Aspect Ratio (EAR) calculation
- Drowsiness detection based on eye closure duration
- Visual monitoring using OpenCV

## Requirements

- Windows 10 or 11
- Python 3.10 or another version compatible with the project's dependencies
- Git
- A working webcam

## Installation and Setup

### 1. Clone the repository

Open Command Prompt (CMD) and run:

```cmd
git clone https://github.com/AhmedSabry345/precrash.git
cd precrash
```

### 2. Create a virtual environment

```cmd
python -m venv venv
```

### 3. Install dependencies

If the repository contains `requirements.txt`, run:

```cmd
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Run the program

```cmd
venv\Scripts\python.exe face_model.py
```

Make sure your webcam is connected and accessible before starting the program.

## Quick Start

If you already have Python and Git installed, run these commands in CMD:

```cmd
git clone https://github.com/AhmedSabry345/precrash.git
cd precrash
python -m venv venv
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe face_model.py
```

## How It Works

The prototype uses facial landmarks to identify key points around the eyes.

The Eye Aspect Ratio (EAR) estimates whether the eyes are open or closed by measuring distances between specific eye landmarks. When the EAR remains below a defined threshold for a specified duration, the system can flag a possible drowsiness event.

This prototype is intended for experimentation and development. It is not a validated safety system and should not be relied upon as the sole method of detecting driver fatigue.

## Troubleshooting

- **Python is not recognized:** Install Python and enable *Add Python to PATH* during installation.
- **Git is not recognized:** Install Git for Windows.
- **Webcam does not open:** Check camera permissions and close other applications using the webcam.
- **Dependency installation fails:** Confirm that `requirements.txt` exists and that your Python version is compatible with the required packages.
- **MediaPipe installation fails:** Try a supported Python version for your installed MediaPipe release.

## Project

**Repository:** [AhmedSabry345/precrash](https://github.com/AhmedSabry345/precrash)

**Main script:** `face_model.py`

---

*PreCrash AI — Exploring computer vision for predictive road safety.*
