# Gesture Controlled Virtual Mouse

A powerful and intuitive gesture-controlled mouse system using **MediaPipe** hand tracking and **OpenCV**. Control your computer's mouse cursor with simple hand gestures captured through your webcam!

![Python Version](https://img.shields.io/badge/python-3.11.9-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Programming Language and Libraries](#programming-languague-and-libraries)
- [System Architecture](#system-architecture)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [System Requirements](#system-requirements)
- [License](#license)
- [Author](#author)
- [Acknowledgments](#acknowledgments)
- [Documentation](#documentation)

---

## Overview

This project implements a **touchless mouse control system** that uses computer vision and machine learning to recognize hand gestures and translate them into mouse actions. Built with MediaPipe's robust hand tracking solution, it provides an accessible, hygienic, and ergonomic alternative to traditional mouse devices.

### Problem It Solves
- ✅ Provides accessible input for users with physical disabilities
- ✅ Reduces repetitive strain injuries from traditional mouse usage
- ✅ Offers hygienic touchless interaction in shared environments
- ✅ Enables natural gesture-based computer interaction
- ✅ Works with standard webcams - no special hardware required

---

## Features

### Core Gesture Controls
| Gesture | Action | Description |
|---------|--------|-------------|
| Index Finger | **Move Cursor** | Point and move your index finger to control cursor |
| Thumb + Index | **Left Click** | Pinch these fingers together for left click |
| Thumb + Middle | **Right Click** | Pinch these fingers together for right click |
| Hold Pinch + Move | **Drag & Drop** | Keep pinch gesture while moving for drag-drop |
| All 5 Fingers | **Scroll** | Extend all fingers and move up/down to scroll |

### Advanced Features
- **Real-time FPS Monitoring** - Track performance with live FPS counter
- **Interactive Help Overlay** - Press 'H' for on-screen gesture guide
- **Visual Feedback System** - Color-coded indicators for each gesture
- **Smooth Cursor Movement** - Intelligent smoothing algorithm for natural motion
- **Click Cooldown System** - Prevents accidental multiple clicks
- **Session Statistics** - View average FPS and performance metrics
- **Hand Detection Indicator** - Clear visual feedback when hand is tracked
- **Semi-transparent Info Panel** - Non-intrusive status display

---

## Programming Language and Libraries

### Versions and Purpose
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11.9 | Primary programming language |
| **OpenCV** | 4.10.0.84 | Video capture and image processing |
| **MediaPipe** | 0.10.14 | Hand tracking and landmark detection |
| **PyAutoGUI** | 0.9.54 | System-level mouse control |
| **NumPy** | 1.26.4 | Mathematical operations and computations |

### Key Libraries
- **cv2 (OpenCV)**: Webcam access, frame processing, visual overlays
- **mediapipe**: 21-point hand landmark detection and tracking
- **pyautogui**: Cross-platform mouse cursor control and clicking
- **numpy**: Distance calculations and coordinate transformations
- **time**: FPS calculation and gesture cooldown timing
- **logging**: Error handling and warning suppression

---

## System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     User Input Layer                        |
│              (Hand Gestures via Webcam)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Video Capture Layer                        │
│         (OpenCV - Frame Acquisition & Processing)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Hand Tracking Layer                            │
│    (MediaPipe - 21 Landmark Detection & Classification)     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│            Gesture Recognition Layer                        │
│  (Distance Calculations, Finger Counting, Mode Detection)   │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Action Processing Layer                        │
│    (Cursor Smoothing, Click Cooldown, Scroll Handling)      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│               System Control Layer                          │
│        (PyAutoGUI - Mouse Events & Screen Control)          │
└─────────────────────────────────────────────────────────────┘

```

## Setup Instructions

### Prerequisites
- **Python 3.11.9** (or compatible 3.7+)
- **Webcam** (built-in or external, minimum 720p recommended)
- **Operating System**: Windows 10/11
- **Minimum 4GB RAM** (8GB recommended)
- **Secured and Stable Internet connection** (for initial package installation)

### Step 1: Clone the Repository
```bash
git clone https://github.com/mayukh-oss/Virtual-Mouse
cd Virtual-Mouse
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv VirtualEnv3.13

# Activate virtual environment
# On Windows:
./VirtualEnv3.13/Scripts/activate

```

### Step 3: Install Dependencies
```bash
# Upgrade pip (recommended)
 python.exe -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
# Run the main controller module
python gesture_controller.py
```

### Expected Startup Output
```
[CONFIG] Suppressing TensorFlow and MediaPipe warnings...
[CONFIG] ✓ Warnings suppressed successfully

[CONFIG] Loading video capture settings...
[CONFIG] ✓ Camera resolution: 1280x720
[CONFIG] ✓ Target FPS: 60

[GESTURE_UTILS] Loading gesture utility functions...
[GESTURE_UTILS] ✓ All utility functions loaded successfully

[CONTROLLER] Initializing Gesture Controller module...
[CONTROLLER] ✓ MediaPipe hands solution loaded
[CONTROLLER] ✓ Screen resolution detected: 1920x1080

======================================================================
SYSTEM READY - GESTURE CONTROL ACTIVE
======================================================================

    AVAILABLE GESTURES:
    Move Cursor      → Point with index finger
    Left Click       → Pinch thumb + index finger
    Right Click      → Pinch thumb + middle finger
    Drag & Drop      → Hold left click pinch while moving
    Scroll          → Extend all 5 fingers and move up/down

    KEYBOARD CONTROLS:
  Q → Quit program
  H → Show/Hide help overlay
```

---

## Usage Guide

### Starting the Application
1. Ensure your webcam is connected and not in use by other applications
2. Run `python gesture_controller.py`
3. Wait for initialization (you'll see progress indicators)
4. Position your hand in front of the camera (center of frame works best)

### Performing Gestures

#### 1. Moving the Cursor
- Extend your **index finger** and point
- Move your hand to control cursor position
- Keep hand in the central 60% of the frame for best accuracy

#### 2. Left Click
- Bring your **thumb and index finger** together (pinch gesture)
- You'll see a **red line** between fingers when close enough
- Release to stop clicking

#### 3. Right Click
- Bring your **thumb and middle finger** together
- You'll see a **blue line** between fingers
- Quick pinch performs single right-click

#### 4. Drag and Drop
- Pinch **thumb and index** to initiate drag mode
- Move your hand while maintaining the pinch
- Release pinch to drop
- "DRAGGING" indicator appears on screen

#### 5. Scrolling
- Extend **all 5 fingers** clearly
- Move hand **up** to scroll up
- Move hand **down** to scroll down
- "SCROLLING" indicator appears on screen

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| **Q** | Quit the application |
| **H** | Toggle help overlay on/off |

### Tips for Best Performance
1. **Lighting**: Ensure good, even lighting on your hand
2. **Background**: Plain backgrounds improve tracking accuracy
3. **Distance**: Keep hand 1-2 feet from camera
4. **Position**: Center your hand in the frame
5. **Gestures**: Make clear, deliberate gestures
6. **Speed**: Start with slow movements, increase speed as you get comfortable

---

## Testing

### Manual Testing Checklist
- [ ] **Module Loading**: Verify all 3 modules load without errors
- [ ] **Configuration**: Check config validation passes
- [ ] **Hand Detection**: Verify "Hand Detected" appears when hand is visible
- [ ] **Cursor Movement**: Check smooth cursor tracking with index finger
- [ ] **Left Click**: Test pinch gesture triggers single click
- [ ] **Right Click**: Verify thumb-middle pinch opens context menus
- [ ] **Drag and Drop**: Test file/folder dragging in file explorer
- [ ] **Scroll**: Verify 5-finger gesture scrolls web pages
- [ ] **FPS Counter**: Confirm FPS displays and stays above 25 FPS
- [ ] **Help Overlay**: Press 'H' to verify help screen displays
- [ ] **Exit**: Press 'Q' to verify clean shutdown

### Test Cases

#### Test Case 1: Basic Cursor Movement
- **Input**: Move index finger left/right/up/down
- **Expected**: Cursor follows smoothly with minimal lag
- **Pass Criteria**: <100ms latency, smooth motion

#### Test Case 2: Click Accuracy
- **Input**: Perform 10 left-click gestures
- **Expected**: Each gesture triggers exactly one click
- **Pass Criteria**: 100% accuracy, no false positives

#### Test Case 3: Gesture Recognition
- **Input**: Perform each gesture 5 times
- **Expected**: Correct gesture mode displayed each time
- **Pass Criteria**: >90% recognition accuracy

### Known Issues & Limitations
1. **Low Light**: Performance degrades in poor lighting
2. **Complex Backgrounds**: Busy backgrounds may affect tracking
3. **Multiple Hands**: System only tracks one hand
4. **Mirror Mode**: Video is flipped for intuitive control
5. **Screen Edges**: Cursor may be less responsive at screen edges

---

## Project Structure

```
Virtual-Mouse/
│
├── config.py                  # Configuration module (250+ lines)
│   ├── Environment setup      # Warning suppression
│   ├── Video capture config   # Camera settings
│   ├── MediaPipe settings     # Hand tracking parameters
│   ├── Cursor control         # Smoothing and mapping
│   ├── Gesture thresholds     # Click/scroll detection
│   ├── UI configuration       # Colors, fonts, sizes
│   ├── Keyboard shortcuts     # Key bindings
│   └── Validation logic       # Config verification
│
├── gesture_utils.py           # Utility functions module (450+ lines)
│   ├── get_distance()         # Euclidean distance calculation
│   ├── count_extended_fingers() # Finger extension detection
│   ├── draw_info_panel()      # FPS and mode display
│   ├── show_help_overlay()    # Help screen rendering
│   ├── draw_hand_detected_indicator() # Detection status
│   ├── draw_gesture_indicator()  # Gesture mode display
│   └── draw_drag_indicator()  # Drag mode indicator
│
├── gesture_controller.py      # Main application module (600+ lines)
│   ├── Initialization         # Setup webcam and MediaPipe
│   ├── Main processing loop   # Core gesture recognition
│   │   ├── Frame capture      # Video input
│   │   ├── FPS calculation    # Performance monitoring
│   │   ├── Hand detection     # MediaPipe processing
│   │   ├── Gesture recognition # Classify hand poses
│   │   ├── Mouse control      # PyAutoGUI actions
│   │   └── UI rendering       # Visual feedback
│   ├── Error handling         # Graceful error management
│   └── Resource cleanup       # Memory and resource release
│
├── requirements.txt           # Python dependencies with versions
├── README.md                 # This comprehensive documentation
├── PROJECT_REPORT.md         # Complete project report
├── .gitignore               # Git ignore patterns

```

### Module Description

#### 1. **config.py** - Configuration Module
- **Purpose**: Centralized configuration management
- **Size**: ~250 lines
- **Key Features**:
  - Suppresses TensorFlow/MediaPipe warnings
  - Configures camera resolution (1280x720)
  - Sets MediaPipe confidence thresholds (0.8)
  - Defines gesture detection parameters
  - Validates configuration values
- **Initialization Output**: 70+ print statements showing setup progress

#### 2. **gesture_utils.py** - Utilities Module
- **Purpose**: Reusable helper functions
- **Size**: ~450 lines
- **Functions**: 7 core utility functions
- **Key Features**:
  - Pure functions (no side effects)
  - Comprehensive docstrings
  - Mathematical formulas explained
  - UI rendering functions
- **Usage**: Imported by gesture_controller.py

#### 3. **gesture_controller.py** - Main Controller
- **Purpose**: Application entry point and main logic
- **Size**: ~600 lines
- **Key Features**:
  - Webcam initialization and configuration
  - MediaPipe hand tracking setup
  - 11-step main processing loop
  - Real-time gesture recognition
  - Mouse control via PyAutoGUI
  - Comprehensive error handling
- **Execution**: `python gesture_controller.py`

### Code Statistics
- **Total Lines**: 1,300+ lines across 3 modules
- **Functions**: 7 utility functions + 1 main function
- **Comments**: 600+ lines (46% documentation)
- **Print Statements**: 200+ for detailed logging
- **Modules**: 3 well-separated concerns
- **Average Cyclomatic Complexity**: 5 (maintainable)
  
---

## License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Author

**Your Name**
-  Institution: VIT Bhopal University
-  Email: mayukh.25bai11291@vitbhopal.ac.in
-  GitHub: [https://github.com/mayukh-oss](https://github.com/mayukh-oss)

---

## Acknowledgments

- **MediaPipe Team** - For the excellent hand tracking solution
- **OpenCV Community** - For the comprehensive computer vision library
- **PyAutoGUI Developers** - For the cross-platform automation tool
- **Python Community** - For the amazing ecosystem
- **VIT Bhopal** - For academic support and resources

---

## References

### Technical Documentation
1. [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html) - Official MediaPipe documentation
2. [OpenCV Documentation](https://docs.opencv.org/) - OpenCV API reference
3. [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/) - GUI automation guide
4. [NumPy Documentation](https://numpy.org/doc/) - NumPy user guide

---

## Project Statistics

- **Total Lines of Code**: 1,300+
- **Modules**: 3 (config, utils, controller)
- **Functions**: 8 major functions
- **Dependencies**: 4 core packages
- **Development Time**: 5+ hours
- **Documentation**: Comprehensive (README, statement, project report)
- **Comment Statements**: 600+ comment lines
- **Print Statements**: 200+ for detailed logging

---

*Last Updated: November 2025*

---

## Features

### Gesture Controls
- **Cursor Movement** - Point with your index finger to move the cursor
- **Left Click** - Pinch thumb and index finger together
- **Right Click** - Pinch thumb and middle finger together
- **Drag & Drop** - Hold left click pinch gesture while moving
- **Scroll** - Extend all 5 fingers and move hand up/down

### Advanced Features
- **Real-time FPS Monitoring** - Track performance with live FPS counter
- **Interactive Help Overlay** - Press 'H' for gesture guide
- **Visual Feedback** - Color-coded indicators for each gesture
- **Smooth Cursor Movement** - Intelligent smoothing algorithm
- **Click Cooldown** - Prevents accidental multiple clicks
- **Session Statistics** - View average FPS on program exit

---

## Getting Started

### Prerequisites

- **Python 3.11.9** (or compatible version)
- **Webcam** (built-in or external)
- **Operating System**: Windows

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mayukh-oss/Virtual-Mouse.git
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate

   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start

Run the main program:
```bash
python gesture_controller.py
```

---

## Usage Guide

### Basic Controls

| Gesture | Action | Description |
|---------|--------|-------------|
| Index Finger | Move Cursor | Point and move your index finger |
| Thumb + Index | Left Click | Pinch these fingers together |
| Thumb + Middle | Right Click | Pinch these fingers together |
| Hold Pinch + Move | Drag & Drop | Keep pinch gesture while moving |
| All 5 Fingers | Scroll | Extend all fingers and move up/down |

### Keyboard Controls

| Key | Action |
|-----|--------|
| `Q` | Quit the program |
| `H` | Toggle help overlay |

### Tips for Best Performance

1. **Lighting** - Ensure good lighting for accurate hand detection
2. **Distance** - Keep your hand 1-2 feet from the camera
3. **Position** - Center your hand in the frame for best tracking
4. **Background** - Use a plain background for better detection
5. **Gestures** - Make clear, deliberate gestures for reliable recognition

---

## Project Structure

```
Virtual-Mouse/
│
├── gesture_mouse.py      # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── .gitignore          # Git ignore rules
├── LICENSE             # License file
│
├── logs/               # Log files (created at runtime)
├── screenshots/        # Screenshots (optional)
└── recordings/         # Video recordings (optional)
```

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Dual-core 2.0 GHz | Quad-core 2.5 GHz+ |
| **RAM** | 4 GB | 8 GB+ |
| **Webcam** | 720p @ 30fps | 1080p @ 60fps |
| **Python** | 3.7+ | 3.11.9 |

---

## License

This project is licensed under the MIT License.

---

## Author

**Mayukh Ghosh**
- GitHub: [https://github.com/mayukh-oss](https://github.com/mayukh-oss)
- Email: mayukh.25bai11291@viitbhopal.ac.in

---

## Acknowledgments

- **MediaPipe** - Google's hand tracking solution
- **OpenCV** - Computer vision library
- **PyAutoGUI** - GUI automation library
- **NumPy** - Scientific computing library

---

## Documentation

For more detailed documentation, visit:
- [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)

---
