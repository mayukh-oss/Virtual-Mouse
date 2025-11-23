# ============================================================================
# GESTURE_CONTROLLER.PY - Main Gesture Control Logic
# ============================================================================
# This module contains the main application logic for the gesture-controlled
# virtual mouse. It handles video capture, hand detection, gesture recognition,
# and mouse control operations.
# ============================================================================

# Import required libraries
import cv2  # OpenCV for video capture and display
import mediapipe as mp  # MediaPipe for hand tracking
import pyautogui  # PyAutoGUI for mouse control
import numpy as np  # NumPy for numerical operations
import time  # Time module for FPS calculation and cooldowns

# Import our custom modules
from config import *  # Import all configuration constants
from gesture_utils import *  # Import all utility functions

# Print module initialization message
print("\n[CONTROLLER] Initializing Gesture Controller module...")

# ============================================================================
# INITIALIZE MEDIAPIPE HAND TRACKING
# ============================================================================

print("\n[CONTROLLER] Setting up MediaPipe Hand Tracking...")

# Access MediaPipe's hands solution
# This provides pre-trained models for hand landmark detection
mp_hands = mp.solutions.hands
print("[CONTROLLER] ✓ MediaPipe hands solution loaded")

# Access MediaPipe's drawing utilities
# This helps us draw hand landmarks and connections on the video frame
mp_drawing = mp.solutions.drawing_utils
print("[CONTROLLER] ✓ MediaPipe drawing utilities loaded")

# ============================================================================
# CONFIGURE PYAUTOGUI
# ============================================================================

print("\n[CONTROLLER] Configuring PyAutoGUI for mouse control...")

# Disable PyAutoGUI failsafe
# Failsafe: moving mouse to screen corner aborts program (we disable this)
pyautogui.FAILSAFE = PYAUTOGUI_FAILSAFE
print(f"[CONTROLLER] ✓ PyAutoGUI failsafe: {PYAUTOGUI_FAILSAFE}")

# Set minimal pause between PyAutoGUI commands for smooth operation
pyautogui.PAUSE = PYAUTOGUI_PAUSE
print(f"[CONTROLLER] ✓ PyAutoGUI pause: {PYAUTOGUI_PAUSE}s")

# Get screen dimensions for coordinate mapping
screen_width, screen_height = pyautogui.size()
print(f"[CONTROLLER] ✓ Screen resolution detected: {screen_width}x{screen_height}")

# ============================================================================
# INITIALIZE GLOBAL STATE VARIABLES
# ============================================================================

print("\n[CONTROLLER] Initializing state variables...")

# Cursor smoothing variables
# These store the previous cursor position for smooth movement
prev_cursor_x = 0  # Previous X coordinate of cursor
prev_cursor_y = 0  # Previous Y coordinate of cursor
print("[CONTROLLER] ✓ Cursor position initialized: (0, 0)")

# Gesture state variables
drag_mode = False  # Boolean: True when dragging, False otherwise
last_click_time = 0  # Timestamp of last click (for cooldown)
gesture_mode = MODE_CURSOR  # Current gesture mode (starts with CURSOR)
scroll_start_y = 0  # Y position when scroll started (for delta calculation)
print(f"[CONTROLLER] ✓ Initial gesture mode: {gesture_mode}")

# Performance monitoring variables
prev_frame_time = 0  # Timestamp of previous frame (for FPS calculation)
fps_history = []  # List storing recent FPS values for averaging
print("[CONTROLLER] ✓ Performance monitoring initialized")

print("\n[CONTROLLER] ✓ All state variables initialized")


# ============================================================================
# MAIN GESTURE CONTROL FUNCTION
# ============================================================================

def main():
    """
    Main function that runs the gesture-controlled mouse application.

    This function:
    1. Initializes the webcam
    2. Creates MediaPipe hand detector
    3. Enters main loop to:
       - Capture video frames
       - Detect hand landmarks
       - Recognize gestures
       - Control mouse cursor
       - Display visual feedback
    4. Handles cleanup on exit

    Returns:
        None
    """
    # Declare global variables that we'll modify in this function
    global prev_cursor_x, prev_cursor_y, drag_mode, last_click_time
    global gesture_mode, scroll_start_y, prev_frame_time, fps_history

    print("\n" + "=" * 70)
    print("STARTING GESTURE MOUSE CONTROLLER")
    print("=" * 70)

    # ========================================================================
    # INITIALIZE WEBCAM
    # ========================================================================

    print("\n[CONTROLLER] Initializing webcam...")

    # Create VideoCapture object to access the webcam
    # CAMERA_INDEX (usually 0) specifies which camera to use
    cap = cv2.VideoCapture(CAMERA_INDEX)

    # Check if webcam opened successfully
    if not cap.isOpened():
        # If webcam couldn't be opened, print error and exit
        print("[CONTROLLER] ✗ ERROR: Could not open webcam!")
        print("[CONTROLLER] Please check:")
        print("[CONTROLLER]   1. Webcam is connected")
        print("[CONTROLLER]   2. No other application is using the webcam")
        print("[CONTROLLER]   3. Camera permissions are granted")
        return  # Exit the function

    print("[CONTROLLER] ✓ Webcam opened successfully")

    # ========================================================================
    # CONFIGURE WEBCAM SETTINGS
    # ========================================================================

    print("\n[CONTROLLER] Configuring webcam settings...")

    # Set webcam resolution width
    # cv2.CAP_PROP_FRAME_WIDTH is the property ID for frame width
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    print(f"[CONTROLLER] ✓ Resolution width: {CAMERA_WIDTH} pixels")

    # Set webcam resolution height
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    print(f"[CONTROLLER] ✓ Resolution height: {CAMERA_HEIGHT} pixels")

    # Set target frames per second (actual FPS may vary by hardware)
    cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
    print(f"[CONTROLLER] ✓ Target FPS: {TARGET_FPS}")

    # ========================================================================
    # DISPLAY STARTUP INFORMATION
    # ========================================================================

    print("\n" + "=" * 70)
    print("SYSTEM READY - GESTURE CONTROL ACTIVE")
    print("=" * 70)

    print("\n✨ AVAILABLE GESTURES:")
    print("  🖱️  Move Cursor      → Point with index finger")
    print("  👆 Left Click       → Pinch thumb + index finger")
    print("  🖱️  Right Click      → Pinch thumb + middle finger")
    print("  ✊ Drag & Drop      → Hold left click pinch while moving")
    print("  🖐️  Scroll          → Extend all 5 fingers and move up/down")

    print("\n⌨️  KEYBOARD CONTROLS:")
    print("  Q → Quit program")
    print("  H → Show/Hide help overlay")
    print("=" * 70 + "\n")

    # ========================================================================
    # INITIALIZE HELP OVERLAY STATE
    # ========================================================================

    # Boolean to track if help overlay is visible
    show_help = False
    print("[CONTROLLER] ✓ Help overlay: OFF (press 'H' to toggle)")

    # ========================================================================
    # CREATE MEDIAPIPE HANDS DETECTOR
    # ========================================================================

    print("\n[CONTROLLER] Creating MediaPipe Hands detector...")

    # Use context manager (with statement) for proper resource management
    # This ensures MediaPipe resources are cleaned up properly
    with mp_hands.Hands(
            static_image_mode=STATIC_IMAGE_MODE,  # False = video stream mode
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,  # 0.8 = 80% confidence
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,  # 0.8 = 80% confidence
            max_num_hands=MAX_NUM_HANDS,  # Track only 1 hand
            model_complexity=MODEL_COMPLEXITY  # 1 = full model for accuracy
    ) as hands:

        print("[CONTROLLER] ✓ MediaPipe Hands detector created")
        print(f"[CONTROLLER] ✓ Detection confidence: {MIN_DETECTION_CONFIDENCE}")
        print(f"[CONTROLLER] ✓ Tracking confidence: {MIN_TRACKING_CONFIDENCE}")
        print(f"[CONTROLLER] ✓ Max hands: {MAX_NUM_HANDS}")

        print("\n[CONTROLLER] Entering main processing loop...")
        print("[CONTROLLER] System is now active and tracking hand gestures")
        print("-" * 70)

        # ====================================================================
        # MAIN PROCESSING LOOP
        # ====================================================================
        # This loop runs continuously until user quits (presses 'Q')

        while cap.isOpened():
            # ================================================================
            # STEP 1: CAPTURE FRAME FROM WEBCAM
            # ================================================================

            # Read a frame from the webcam
            # ret: boolean indicating if frame was read successfully
            # frame: the actual image data as NumPy array
            ret, frame = cap.read()

            # Check if frame was read successfully
            if not ret:
                # If frame read failed, print error and break loop
                print("\n[CONTROLLER] ✗ ERROR: Failed to read frame from webcam")
                print("[CONTROLLER] Breaking main loop...")
                break

            # ================================================================
            # STEP 2: CALCULATE FPS (FRAMES PER SECOND)
            # ================================================================

            # Get current timestamp in seconds
            current_time = time.time()

            # Calculate FPS: 1 / (time between frames)
            # If this is the first frame (prev_frame_time=0), FPS will be 0
            if prev_frame_time != 0:
                fps = 1 / (current_time - prev_frame_time)
            else:
                fps = 0

            # Update previous frame time for next iteration
            prev_frame_time = current_time

            # Add current FPS to history for averaging
            fps_history.append(fps)

            # Keep only last FPS_HISTORY_SIZE values (e.g., last 30 frames)
            if len(fps_history) > FPS_HISTORY_SIZE:
                fps_history.pop(0)  # Remove oldest FPS value

            # Calculate average FPS for smoother display
            avg_fps = sum(fps_history) / len(fps_history) if fps_history else 0

            # ================================================================
            # STEP 3: PREPROCESS FRAME
            # ================================================================

            # Flip frame horizontally (mirror effect)
            # This makes the interaction more intuitive: moving hand right moves cursor right
            frame = cv2.flip(frame, 1)

            # Get frame dimensions (height, width, channels)
            frame_height, frame_width, _ = frame.shape

            # Convert frame from BGR (OpenCV format) to RGB (MediaPipe format)
            # OpenCV uses BGR color order, MediaPipe expects RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # ================================================================
            # STEP 4: PROCESS FRAME WITH MEDIAPIPE
            # ================================================================

            # Process the RGB frame to detect hands
            # Returns a results object containing detected hand landmarks
            results = hands.process(rgb_frame)

            # ================================================================
            # STEP 5: RESET GESTURE MODE
            # ================================================================

            # Reset gesture mode to CURSOR at start of each frame
            # Will be updated if specific gesture is detected
            gesture_mode = MODE_CURSOR

            # ================================================================
            # STEP 6: CHECK IF HAND WAS DETECTED
            # ================================================================

            if results.multi_hand_landmarks:
                # Hand detected! Draw indicator in top-right
                draw_hand_detected_indicator(frame, frame_width)

                # ============================================================
                # STEP 7: PROCESS DETECTED HAND
                # ============================================================

                # Iterate through each detected hand
                # (In our case, usually just one since MAX_NUM_HANDS=1)
                for hand_landmarks in results.multi_hand_landmarks:

                    # ========================================================
                    # STEP 7A: DRAW HAND SKELETON
                    # ========================================================

                    # Draw hand landmarks and connections on the frame
                    mp_drawing.draw_landmarks(
                        frame,  # Image to draw on
                        hand_landmarks,  # The 21 hand landmarks
                        mp_hands.HAND_CONNECTIONS,  # Lines connecting landmarks
                        # Landmark style: green circles, 2px thick, radius 2
                        mp_drawing.DrawingSpec(
                            color=COLOR_GREEN, thickness=2, circle_radius=2
                        ),
                        # Connection style: red lines, 2px thick
                        mp_drawing.DrawingSpec(
                            color=COLOR_RED, thickness=2
                        )
                    )

                    # ========================================================
                    # STEP 7B: EXTRACT HAND LANDMARKS
                    # ========================================================

                    # Get the landmarks list (21 points)
                    landmarks = hand_landmarks.landmark

                    # ========================================================
                    # STEP 7C: GET FINGER TIP POSITIONS
                    # ========================================================

                    # Get INDEX finger tip (landmark 8)
                    index_tip = landmarks[INDEX_TIP]
                    # Convert normalized coordinates (0-1) to pixel coordinates
                    index_x = int(index_tip.x * frame_width)
                    index_y = int(index_tip.y * frame_height)

                    # Get MIDDLE finger tip (landmark 12)
                    middle_tip = landmarks[MIDDLE_TIP]
                    middle_x = int(middle_tip.x * frame_width)
                    middle_y = int(middle_tip.y * frame_height)

                    # Get THUMB tip (landmark 4)
                    thumb_tip = landmarks[THUMB_TIP]
                    thumb_x = int(thumb_tip.x * frame_width)
                    thumb_y = int(thumb_tip.y * frame_height)

                    # ========================================================
                    # STEP 7D: MAP HAND POSITION TO SCREEN COORDINATES
                    # ========================================================

                    # Calculate control area boundaries
                    # We use only the middle 60% of the frame for better control
                    control_start_x = int(frame_width * CONTROL_AREA_START)
                    control_end_x = int(frame_width * CONTROL_AREA_END)
                    control_start_y = int(frame_height * CONTROL_AREA_START)
                    control_end_y = int(frame_height * CONTROL_AREA_END)

                    # Map index finger position to screen coordinates
                    # np.interp: linear interpolation between ranges
                    screen_x = np.interp(
                        index_x,  # Input value (hand x-position)
                        [control_start_x, control_end_x],  # Input range
                        [0, screen_width]  # Output range (screen width)
                    )

                    screen_y = np.interp(
                        index_y,  # Input value (hand y-position)
                        [control_start_y, control_end_y],  # Input range
                        [0, screen_height]  # Output range (screen height)
                    )

                    # ========================================================
                    # STEP 7E: SMOOTH CURSOR MOVEMENT
                    # ========================================================

                    # Apply exponential moving average for smooth cursor movement
                    # Formula: new = old + (target - old) / smoothing_factor
                    # Higher smoothing = smoother but slower response
                    curr_x = prev_cursor_x + (screen_x - prev_cursor_x) / SMOOTHING_FACTOR
                    curr_y = prev_cursor_y + (screen_y - prev_cursor_y) / SMOOTHING_FACTOR

                    # Move the actual mouse cursor to the calculated position
                    pyautogui.moveTo(curr_x, curr_y)

                    # Update previous cursor position for next frame
                    prev_cursor_x, prev_cursor_y = curr_x, curr_y

                    # ========================================================
                    # STEP 7F: CALCULATE DISTANCES FOR GESTURE DETECTION
                    # ========================================================

                    # Calculate distance between thumb and index finger
                    # Used to detect left-click pinch gesture
                    thumb_index_dist = get_distance(
                        (thumb_x, thumb_y),
                        (index_x, index_y)
                    )

                    # Calculate distance between thumb and middle finger
                    # Used to detect right-click pinch gesture
                    thumb_middle_dist = get_distance(
                        (thumb_x, thumb_y),
                        (middle_x, middle_y)
                    )

                    # Count how many fingers are extended
                    # Used to detect scroll gesture (5 fingers)
                    extended_fingers = count_extended_fingers(
                        landmarks,
                        frame_width,
                        frame_height
                    )

                    # ========================================================
                    # STEP 7G: GESTURE RECOGNITION
                    # ========================================================

                    # Get current time for cooldown checks
                    current_gesture_time = time.time()

                    # --------------------------------------------------------
                    # GESTURE 1: LEFT CLICK (Thumb + Index Pinch)
                    # --------------------------------------------------------

                    if thumb_index_dist < CLICK_THRESHOLD:
                        # Pinch detected! Update gesture mode
                        gesture_mode = MODE_LEFT_CLICK

                        # Draw red line between thumb and index
                        cv2.line(
                            frame,
                            (thumb_x, thumb_y),  # Start point (thumb)
                            (index_x, index_y),  # End point (index)
                            COLOR_RED,  # Red color for left click
                            3  # Line thickness
                        )

                        # Check if enough time has passed since last click (cooldown)
                        if current_gesture_time - last_click_time > CLICK_COOLDOWN:
                            # If not already in drag mode, perform a click
                            if not drag_mode:
                                # Execute left mouse button click
                                pyautogui.click()
                                # Update last click time
                                last_click_time = current_gesture_time
                                # Log the click action
                                print(f"[{time.strftime('%H:%M:%S')}] LEFT CLICK performed")
                            # Enter drag mode (will stay in drag until pinch released)
                            drag_mode = True

                    # --------------------------------------------------------
                    # GESTURE 2: RIGHT CLICK (Thumb + Middle Pinch)
                    # --------------------------------------------------------

                    elif thumb_middle_dist < CLICK_THRESHOLD:
                        # Pinch detected! Update gesture mode
                        gesture_mode = MODE_RIGHT_CLICK

                        # Draw blue line between thumb and middle finger
                        cv2.line(
                            frame,
                            (thumb_x, thumb_y),  # Start point (thumb)
                            (middle_x, middle_y),  # End point (middle)
                            COLOR_BLUE,  # Blue color for right click
                            3  # Line thickness
                        )

                        # Check cooldown before performing right click
                        if current_gesture_time - last_click_time > CLICK_COOLDOWN:
                            # Execute right mouse button click
                            pyautogui.rightClick()
                            # Update last click time
                            last_click_time = current_gesture_time
                            # Log the click action
                            print(f"[{time.strftime('%H:%M:%S')}] RIGHT CLICK performed")

                    # --------------------------------------------------------
                    # GESTURE 3: SCROLL (All 5 Fingers Extended)
                    # --------------------------------------------------------

                    elif extended_fingers == 5:
                        # All fingers extended! Update gesture mode
                        gesture_mode = MODE_SCROLL

                        # Initialize scroll start position if not set
                        if scroll_start_y == 0:
                            scroll_start_y = index_y

                        # Calculate vertical movement since scroll started
                        scroll_delta = scroll_start_y - index_y

                        # Only scroll if movement exceeds threshold
                        if abs(scroll_delta) > SCROLL_THRESHOLD:
                            # Calculate scroll amount (scale down by factor of 10)
                            scroll_amount = int(scroll_delta / 10)
                            # Execute scroll action
                            # Positive = scroll up, Negative = scroll down
                            pyautogui.scroll(scroll_amount)
                            # Update scroll start position
                            scroll_start_y = index_y
                            # Log the scroll action
                            print(f"[{time.strftime('%H:%M:%S')}] SCROLL: {scroll_amount}")

                        # Draw scrolling indicator
                        draw_gesture_indicator(
                            frame, MODE_SCROLL, frame_width, frame_height
                        )

                    # --------------------------------------------------------
                    # NO SPECIFIC GESTURE DETECTED
                    # --------------------------------------------------------

                    else:
                        # If we were in drag mode, release it
                        if drag_mode:
                            drag_mode = False
                            print(f"[{time.strftime('%H:%M:%S')}] DRAG released")

                        # Reset scroll start position
                        scroll_start_y = 0

                        # Draw green line between thumb and index (default)
                        cv2.line(
                            frame,
                            (thumb_x, thumb_y),
                            (index_x, index_y),
                            COLOR_GREEN,  # Green = no active gesture
                            2  # Thinner line for default state
                        )

                    # ========================================================
                    # STEP 7H: DRAW VISUAL MARKERS ON FINGERS
                    # ========================================================

                    # Draw blue circle on index finger tip
                    cv2.circle(
                        frame,
                        (index_x, index_y),  # Center position
                        LANDMARK_CIRCLE_RADIUS,  # Radius (12 pixels)
                        COLOR_BLUE,  # Blue color
                        -1  # Filled circle
                    )

                    # Draw orange circle on middle finger tip
                    cv2.circle(
                        frame,
                        (middle_x, middle_y),
                        10,  # Slightly smaller radius
                        COLOR_ORANGE,  # Orange color
                        -1  # Filled
                    )

                    # Draw green circle on thumb tip
                    cv2.circle(
                        frame,
                        (thumb_x, thumb_y),
                        LANDMARK_CIRCLE_RADIUS,
                        COLOR_GREEN,  # Green color
                        -1  # Filled
                    )

                    # ========================================================
                    # STEP 7I: DRAW DRAG MODE INDICATOR
                    # ========================================================

                    # If in drag mode, show indicator
                    if drag_mode:
                        draw_drag_indicator(frame, frame_width, frame_height)

            # ================================================================
            # STEP 8: DRAW INFO PANEL
            # ================================================================

            # Draw the information panel with FPS and mode
            draw_info_panel(frame, avg_fps, gesture_mode, frame_width, frame_height)

            # ================================================================
            # STEP 9: DRAW HELP OVERLAY IF ENABLED
            # ================================================================

            # If help is toggled on, show the help overlay
            if show_help:
                show_help_overlay(frame, frame_width, frame_height)

            # ================================================================
            # STEP 10: DISPLAY THE FRAME
            # ================================================================

            # Show the processed frame in a window
            cv2.imshow(WINDOW_TITLE, frame)

            # ================================================================
            # STEP 11: CHECK FOR KEYBOARD INPUT
            # ================================================================

            # Wait 1ms for keyboard input
            # cv2.waitKey returns -1 if no key pressed, otherwise the key code
            key = cv2.waitKey(1) & 0xFF

            # Check if 'Q' key was pressed (quit)
            if key == KEY_QUIT:
                print("\n" + "=" * 70)
                print("EXITING PROGRAM - User pressed 'Q'")
                print("=" * 70)
                break  # Exit the main loop

            # Check if 'H' key was pressed (toggle help)
            elif key == KEY_HELP:
                # Toggle help overlay state
                show_help = not show_help
                # Log the state change
                status = "ON" if show_help else "OFF"
                print(f"[{time.strftime('%H:%M:%S')}] Help overlay: {status}")

        # End of main loop
        print("\n[CONTROLLER] Exited main processing loop")

    # ========================================================================
    # CLEANUP
    # ========================================================================

    print("\n[CONTROLLER] Cleaning up resources...")

    # Calculate and display session statistics
    if fps_history:
        avg_session_fps = int(sum(fps_history) / len(fps_history))
        print(f"[CONTROLLER] ✓ Average FPS during session: {avg_session_fps}")

    # Release the webcam resource
    cap.release()
    print("[CONTROLLER] ✓ Webcam released")

    # Close all OpenCV windows
    cv2.destroyAllWindows()
    print("[CONTROLLER] ✓ All windows closed")

    print("[CONTROLLER] ✓ Resources released successfully")
    print("\n" + "=" * 70)
    print("Program terminated. Thank you for using Gesture Mouse Control!")
    print("=" * 70)


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    This block only runs if this file is executed directly
    (not imported as a module).

    It handles:
    1. Normal execution
    2. Keyboard interrupt (Ctrl+C)
    3. Unexpected errors
    """

    print("\n" + "=" * 70)
    print("GESTURE CONTROLLED VIRTUAL MOUSE")
    print("=" * 70)

    try:
        # ====================================================================
        # NORMAL EXECUTION
        # ====================================================================

        # Call the main function to start the application
        main()

    except KeyboardInterrupt:
        # ====================================================================
        # HANDLE KEYBOARD INTERRUPT (Ctrl+C)
        # ====================================================================

        # User pressed Ctrl+C to stop the program
        print("\n\n" + "=" * 70)
        print("PROGRAM INTERRUPTED - User pressed Ctrl+C")
        print("=" * 70)
        print("\nShutting down gracefully...")

        # Close all OpenCV windows
        cv2.destroyAllWindows()

        print("✓ Program terminated successfully")
        print("=" * 70)

    except Exception as e:
        # ====================================================================
        # HANDLE UNEXPECTED ERRORS
        # ====================================================================

        # An unexpected error occurred
        print("\n" + "=" * 70)
        print("✗ ERROR OCCURRED!")
        print("=" * 70)
        print(f"\nError Details: {str(e)}")
        print(f"Error Type: {type(e).__name__}")

        # Print troubleshooting information
        print("\nTroubleshooting:")
        print("  1. Make sure your webcam is connected and not in use")
        print("  2. Check if all required libraries are installed:")
        print("     pip install opencv-python mediapipe pyautogui numpy")
        print("  3. Ensure you have proper permissions to access the webcam")
        print("  4. Try restarting the application")
        print("  5. Check if your Python version is 3.7 or higher")
        print("=" * 70)

        # Close all windows even on error
        cv2.destroyAllWindows()

print("\n[CONTROLLER] ✓ Module loaded and ready")
print("=" * 70)