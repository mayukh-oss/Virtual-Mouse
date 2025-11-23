# ============================================================================
# CONFIG.PY - Configuration Module
# ============================================================================
# This module contains all configuration parameters and constants used
# throughout the Gesture Controlled Virtual Mouse application.
# Centralizing configuration makes it easy to tune the system without
# modifying core logic in multiple places.
# ============================================================================

# Import required libraries for environment setup
import os  # Operating system interface for environment variables
import warnings  # Warning control for suppressing unnecessary messages
import logging  # Logging framework for error handling

# ============================================================================
# SUPPRESS WARNINGS AND LOGGING
# ============================================================================
# TensorFlow and MediaPipe generate many info/warning messages that clutter
# the console. We suppress these to provide clean output for users.

print("\n[CONFIG] Suppressing TensorFlow and MediaPipe warnings...")

# Set TensorFlow logging level to ERROR only (suppresses INFO and WARNING)
# Level 3 = ERROR, 2 = WARNING, 1 = INFO, 0 = DEBUG
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Disable oneDNN custom operations to prevent optimization warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Filter out UserWarning from google.protobuf module
# This prevents deprecation warnings from protobuf library
warnings.filterwarnings('ignore', category=UserWarning, module='google.protobuf')

# Filter out all DeprecationWarning messages
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Configure logging levels for TensorFlow and MediaPipe
# Only ERROR level messages will be shown
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('mediapipe').setLevel(logging.ERROR)

print("[CONFIG] ✓ Warnings suppressed successfully")

# ============================================================================
# VIDEO CAPTURE CONFIGURATION
# ============================================================================
# Settings for webcam video capture and processing

print("\n[CONFIG] Loading video capture settings...")

# Camera resolution settings
CAMERA_WIDTH = 1280  # Horizontal resolution in pixels
CAMERA_HEIGHT = 720  # Vertical resolution in pixels
# Note: Higher resolution provides better hand detection but requires more processing power

# Target frames per second for video capture
TARGET_FPS = 60  # Request 60 FPS from camera (actual FPS may vary by hardware)

# Camera device index
CAMERA_INDEX = 0  # 0 = default/built-in camera, 1 = first external camera, etc.

print(f"[CONFIG] ✓ Camera resolution: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
print(f"[CONFIG] ✓ Target FPS: {TARGET_FPS}")

# ============================================================================
# MEDIAPIPE HAND TRACKING CONFIGURATION
# ============================================================================
# Settings for MediaPipe hand landmark detection

print("\n[CONFIG] Loading MediaPipe settings...")

# Detection confidence threshold (0.0 to 1.0)
# Higher values = more accurate but may miss some hands
MIN_DETECTION_CONFIDENCE = 0.8  # 80% confidence required for initial hand detection

# Tracking confidence threshold (0.0 to 1.0)
# Higher values = more stable tracking but may lose track more easily
MIN_TRACKING_CONFIDENCE = 0.8  # 80% confidence required to continue tracking

# Maximum number of hands to detect
# Setting to 1 improves performance significantly
MAX_NUM_HANDS = 1  # Track only one hand at a time

# Model complexity: 0 = lite model (faster), 1 = full model (more accurate)
MODEL_COMPLEXITY = 1  # Use full model for better accuracy

# Static image mode: False = video stream (optimized for continuous frames)
STATIC_IMAGE_MODE = False  # Optimized for real-time video processing

print(f"[CONFIG] ✓ Detection confidence: {MIN_DETECTION_CONFIDENCE}")
print(f"[CONFIG] ✓ Tracking confidence: {MIN_TRACKING_CONFIDENCE}")
print(f"[CONFIG] ✓ Max hands to track: {MAX_NUM_HANDS}")
print(f"[CONFIG] ✓ Model complexity: {MODEL_COMPLEXITY}")

# ============================================================================
# CURSOR CONTROL CONFIGURATION
# ============================================================================
# Settings for cursor movement and coordinate mapping

print("\n[CONFIG] Loading cursor control settings...")

# Smoothing factor for cursor movement (1-20)
# Higher values = smoother but slower cursor movement
# Lower values = faster but jerkier cursor movement
SMOOTHING_FACTOR = 7  # Balanced smoothing for natural feel

# Active control area of the camera frame
# Using only the middle portion prevents edge sensitivity issues
CONTROL_AREA_START = 0.2  # Start at 20% from left edge (ignore left 20%)
CONTROL_AREA_END = 0.8    # End at 80% from left edge (ignore right 20%)
# This means the middle 60% of frame controls 100% of screen

# PyAutoGUI pause duration between actions (in seconds)
# Very small value for responsive control
PYAUTOGUI_PAUSE = 0.001  # 1 millisecond pause

# Disable PyAutoGUI failsafe (moving mouse to corner won't stop program)
PYAUTOGUI_FAILSAFE = False

print(f"[CONFIG] ✓ Cursor smoothing factor: {SMOOTHING_FACTOR}")
print(f"[CONFIG] ✓ Active control area: {CONTROL_AREA_START:.0%} to {CONTROL_AREA_END:.0%}")

# ============================================================================
# GESTURE DETECTION CONFIGURATION
# ============================================================================
# Thresholds and parameters for gesture recognition

print("\n[CONFIG] Loading gesture detection settings...")

# Click threshold: maximum distance (in pixels) between fingers for pinch detection
# When thumb and index/middle finger are closer than this, it's considered a pinch
CLICK_THRESHOLD = 40  # 40 pixels - adjust based on camera distance and resolution

# Scroll threshold: minimum vertical movement (in pixels) to trigger scroll
# Hand must move this many pixels up/down before scroll activates
SCROLL_THRESHOLD = 30  # 30 pixels of vertical movement required

# Click cooldown period (in seconds)
# Minimum time between consecutive clicks to prevent accidental double-clicks
CLICK_COOLDOWN = 0.3  # 300 milliseconds between clicks

# Double-click time window (in seconds)
# Maximum time between two clicks to be considered a double-click (future feature)
DOUBLE_CLICK_TIME = 0.5  # 500 milliseconds

print(f"[CONFIG] ✓ Click threshold: {CLICK_THRESHOLD} pixels")
print(f"[CONFIG] ✓ Scroll threshold: {SCROLL_THRESHOLD} pixels")
print(f"[CONFIG] ✓ Click cooldown: {CLICK_COOLDOWN} seconds")

# ============================================================================
# PERFORMANCE MONITORING CONFIGURATION
# ============================================================================
# Settings for FPS tracking and performance monitoring

print("\n[CONFIG] Loading performance monitoring settings...")

# Number of frames to keep in FPS history for averaging
# Larger buffer = smoother FPS display but slower to react to changes
FPS_HISTORY_SIZE = 30  # Average FPS over last 30 frames

print(f"[CONFIG] ✓ FPS averaging window: {FPS_HISTORY_SIZE} frames")

# ============================================================================
# USER INTERFACE CONFIGURATION
# ============================================================================
# Settings for visual feedback and on-screen display

print("\n[CONFIG] Loading UI settings...")

# Info panel dimensions
INFO_PANEL_HEIGHT = 120  # Height of top info panel in pixels

# Font settings
FONT_SCALE_LARGE = 0.7   # Font scale for main text (FPS, Mode)
FONT_SCALE_SMALL = 0.5   # Font scale for small text (instructions)
FONT_THICKNESS = 2       # Font thickness (1-3, higher = bolder)

# Color definitions (BGR format for OpenCV)
COLOR_GREEN = (0, 255, 0)      # Success, active, detected
COLOR_RED = (0, 0, 255)        # Left click, errors
COLOR_BLUE = (255, 0, 0)       # Right click, index finger
COLOR_ORANGE = (0, 165, 255)   # Middle finger, drag mode
COLOR_YELLOW = (0, 255, 255)   # Scroll mode, warnings
COLOR_CYAN = (255, 255, 0)     # Mode indicators
COLOR_WHITE = (255, 255, 255)  # General text
COLOR_BLACK = (0, 0, 0)        # Backgrounds, overlays

# Visual marker sizes
LANDMARK_CIRCLE_RADIUS = 12    # Radius of finger tip circles
CONNECTION_LINE_THICKNESS = 2  # Thickness of lines between fingers

print("[CONFIG] ✓ UI color scheme loaded")
print("[CONFIG] ✓ Font settings configured")

# ============================================================================
# KEYBOARD SHORTCUTS CONFIGURATION
# ============================================================================
# Keyboard control keys for the application

print("\n[CONFIG] Loading keyboard shortcuts...")

# Key codes for application control
KEY_QUIT = ord('q')     # Press 'q' to quit application
KEY_HELP = ord('h')     # Press 'h' to toggle help overlay

print("[CONFIG] ✓ Keyboard shortcuts: 'Q' to quit, 'H' for help")

# ============================================================================
# HAND LANDMARK INDICES
# ============================================================================
# MediaPipe hand landmark point indices (21 total landmarks)
# These constants make code more readable than using numbers

print("\n[CONFIG] Loading hand landmark indices...")

# Finger tip landmarks
THUMB_TIP = 4          # Landmark index for thumb tip
INDEX_TIP = 8          # Landmark index for index finger tip
MIDDLE_TIP = 12        # Landmark index for middle finger tip
RING_TIP = 16          # Landmark index for ring finger tip
PINKY_TIP = 20         # Landmark index for pinky finger tip

# Finger joint landmarks (for extension detection)
THUMB_IP = 3           # Thumb interphalangeal joint
INDEX_PIP = 6          # Index finger proximal interphalangeal joint
MIDDLE_PIP = 10        # Middle finger PIP joint
RING_PIP = 14          # Ring finger PIP joint
PINKY_PIP = 18         # Pinky finger PIP joint

# Lists for iteration
FINGER_TIPS = [INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]  # All finger tips except thumb
FINGER_PIPS = [INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP]  # Corresponding PIP joints

print("[CONFIG] ✓ Hand landmark indices configured")

# ============================================================================
# GESTURE MODE CONSTANTS
# ============================================================================
# String constants for different gesture modes

# Mode names (for display and logic)
MODE_CURSOR = "CURSOR"           # Default cursor movement mode
MODE_LEFT_CLICK = "LEFT CLICK"   # Left mouse button click mode
MODE_RIGHT_CLICK = "RIGHT CLICK" # Right mouse button click mode
MODE_SCROLL = "SCROLL"           # Scroll wheel mode
MODE_DRAG = "DRAG"               # Drag and drop mode

print("[CONFIG] ✓ Gesture modes defined")

# ============================================================================
# WINDOW CONFIGURATION
# ============================================================================
# Settings for OpenCV display window

# Window title
WINDOW_TITLE = "Gesture Mouse Control - Enhanced"

print(f"[CONFIG] ✓ Window title: {WINDOW_TITLE}")

# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================
# Validate configuration values are within acceptable ranges

print("\n[CONFIG] Validating configuration values...")

# Validate smoothing factor
if SMOOTHING_FACTOR < 1 or SMOOTHING_FACTOR > 20:
    print(f"[CONFIG] ⚠ WARNING: SMOOTHING_FACTOR ({SMOOTHING_FACTOR}) outside recommended range (1-20)")
else:
    print(f"[CONFIG] ✓ Smoothing factor valid: {SMOOTHING_FACTOR}")

# Validate confidence thresholds
if not (0.0 <= MIN_DETECTION_CONFIDENCE <= 1.0):
    print(f"[CONFIG] ⚠ WARNING: MIN_DETECTION_CONFIDENCE ({MIN_DETECTION_CONFIDENCE}) must be 0.0-1.0")
if not (0.0 <= MIN_TRACKING_CONFIDENCE <= 1.0):
    print(f"[CONFIG] ⚠ WARNING: MIN_TRACKING_CONFIDENCE ({MIN_TRACKING_CONFIDENCE}) must be 0.0-1.0")

# Validate control area
if not (0.0 <= CONTROL_AREA_START < CONTROL_AREA_END <= 1.0):
    print(f"[CONFIG] ⚠ WARNING: Invalid control area: {CONTROL_AREA_START}-{CONTROL_AREA_END}")
else:
    print(f"[CONFIG] ✓ Control area valid: {CONTROL_AREA_START:.0%}-{CONTROL_AREA_END:.0%}")

print("\n[CONFIG] ✓ Configuration module loaded successfully")
print("=" * 70)