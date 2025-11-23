# ============================================================================
# GESTURE_UTILS.PY - Gesture Recognition Utilities
# ============================================================================
# This module contains utility functions for gesture recognition, distance
# calculation, finger counting, and visual rendering of UI elements.
# These functions are pure and reusable across the application.
# ============================================================================

# Import required libraries
import cv2  # OpenCV for drawing and image operations
import numpy as np  # NumPy for mathematical calculations
from config import *  # Import all configuration constants

# Print module initialization message
print("\n[GESTURE_UTILS] Loading gesture utility functions...")


# ============================================================================
# DISTANCE CALCULATION FUNCTION
# ============================================================================

def get_distance(p1, p2):
    """
    Calculate the Euclidean distance between two points in 2D space.

    This function is used to determine how close two fingers are to each other,
    which is essential for detecting pinch gestures (thumb-index, thumb-middle).

    Parameters:
        p1 (tuple): First point as (x, y) coordinates
        p2 (tuple): Second point as (x, y) coordinates

    Returns:
        float: The Euclidean distance between the two points in pixels

    Mathematical Formula:
        distance = sqrt((x2 - x1)² + (y2 - y1)²)

    Example:
        >>> get_distance((0, 0), (3, 4))
        5.0
        >>> get_distance((100, 100), (100, 150))
        50.0
    """
    # Extract x and y coordinates from the first point
    x1, y1 = p1[0], p1[1]

    # Extract x and y coordinates from the second point
    x2, y2 = p2[0], p2[1]

    # Calculate the difference in x coordinates
    dx = x2 - x1

    # Calculate the difference in y coordinates
    dy = y2 - y1

    # Apply the Pythagorean theorem to find the distance
    # sqrt(dx² + dy²) gives us the straight-line distance
    distance = np.sqrt(dx ** 2 + dy ** 2)

    # Return the calculated distance
    return distance


# ============================================================================
# FINGER COUNTING FUNCTION
# ============================================================================

def count_extended_fingers(landmarks, frame_width, frame_height):
    """
    Count the number of extended fingers in the detected hand.

    This function determines if each finger is extended by comparing the
    position of the fingertip with the position of the finger's PIP joint.
    An extended finger has its tip higher (lower y-value) than its joint.

    Parameters:
        landmarks: MediaPipe hand landmarks object containing 21 3D points
        frame_width (int): Width of the video frame in pixels
        frame_height (int): Height of the video frame in pixels

    Returns:
        int: Number of extended fingers (0-5)

    Logic:
        - Thumb: Extended if tip is to the left of IP joint (different from fingers)
        - Other fingers: Extended if tip y-coordinate < PIP joint y-coordinate

    Use Case:
        This is primarily used to detect the 5-finger scroll gesture.
    """
    # Initialize counter for extended fingers
    extended_count = 0

    # ========================================================================
    # CHECK THUMB (Special Case)
    # ========================================================================
    # The thumb moves horizontally rather than vertically, so we check
    # if the thumb tip is to the left of the thumb IP joint

    # Get the thumb tip landmark (landmark index 4)
    thumb_tip = landmarks[THUMB_TIP]

    # Get the thumb IP (interphalangeal) joint landmark (landmark index 3)
    thumb_ip = landmarks[THUMB_IP]

    # Check if thumb is extended
    # For a right hand in mirror view, thumb tip should be LEFT of IP joint
    # This means thumb_tip.x < thumb_ip.x indicates extension
    if thumb_tip.x < thumb_ip.x:
        extended_count += 1  # Increment counter if thumb is extended
        # print(f"[GESTURE_UTILS] Thumb detected as extended")  # Debug output

    # ========================================================================
    # CHECK OTHER FOUR FINGERS (Index, Middle, Ring, Pinky)
    # ========================================================================
    # These fingers move vertically, so we compare y-coordinates
    # Remember: In image coordinates, y increases downward
    # So a lower y value means higher on screen (extended finger)

    # Iterate through each finger using zip to pair tips with joints
    for tip_id, pip_id in zip(FINGER_TIPS, FINGER_PIPS):
        # Get the fingertip landmark
        tip = landmarks[tip_id]

        # Get the PIP (Proximal Interphalangeal) joint landmark
        pip = landmarks[pip_id]

        # Check if finger is extended
        # If tip y-coordinate < PIP y-coordinate, finger is extended upward
        if tip.y < pip.y:
            extended_count += 1  # Increment counter for this extended finger
            # Map landmark ID to finger name for debugging
            # finger_names = {8: "Index", 12: "Middle", 16: "Ring", 20: "Pinky"}
            # print(f"[GESTURE_UTILS] {finger_names[tip_id]} finger detected as extended")

    # Return the total count of extended fingers (0 to 5)
    return extended_count


# ============================================================================
# INFO PANEL DRAWING FUNCTION
# ============================================================================

def draw_info_panel(frame, fps, gesture_mode, frame_width, frame_height):
    """
    Draw a semi-transparent information panel at the top of the frame.

    This panel displays:
    - Current FPS (frames per second)
    - Current gesture mode (CURSOR, LEFT CLICK, RIGHT CLICK, SCROLL, DRAG)
    - Keyboard shortcuts reminder

    Parameters:
        frame (numpy.ndarray): The video frame to draw on (modified in-place)
        fps (float): Current frames per second to display
        gesture_mode (str): Current gesture mode being detected
        frame_width (int): Width of the frame in pixels
        frame_height (int): Height of the frame in pixels

    Returns:
        None (frame is modified in-place)

    Visual Design:
        - Semi-transparent black background (60% opacity)
        - Green text for FPS (indicating active/good performance)
        - Cyan/Orange text for mode (color depends on mode)
        - White text for instructions
    """
    # ========================================================================
    # CREATE SEMI-TRANSPARENT OVERLAY
    # ========================================================================
    # Make a copy of the frame to create the overlay effect
    overlay = frame.copy()

    # Draw a filled black rectangle for the info panel background
    # Coordinates: (x1, y1) = top-left, (x2, y2) = bottom-right
    cv2.rectangle(
        overlay,  # Draw on the overlay copy
        (0, 0),  # Top-left corner (x=0, y=0)
        (frame_width, INFO_PANEL_HEIGHT),  # Bottom-right corner
        COLOR_BLACK,  # Black color
        -1  # -1 means filled rectangle (not just outline)
    )

    # Blend the overlay with the original frame to create transparency
    # Formula: output = overlay * alpha + frame * beta + gamma
    # alpha=0.6 (60% overlay) + beta=0.4 (40% original) = semi-transparent
    cv2.addWeighted(
        overlay, 0.6,  # Overlay image with 60% weight
        frame, 0.4,  # Original frame with 40% weight
        0,  # Gamma (brightness adjustment, 0 = none)
        frame  # Output is written back to original frame
    )

    # ========================================================================
    # DRAW FPS COUNTER
    # ========================================================================
    # Display the current frames per second in the top-left

    # Format FPS as integer for cleaner display
    fps_text = f"FPS: {int(fps)}"

    # Draw the FPS text on the frame
    cv2.putText(
        frame,  # Image to draw on
        fps_text,  # Text to display
        (10, 30),  # Position (x=10, y=30 from top-left)
        cv2.FONT_HERSHEY_SIMPLEX,  # Font type (clean, readable)
        FONT_SCALE_LARGE,  # Font size (0.7 scale)
        COLOR_GREEN,  # Green color (good/active status)
        FONT_THICKNESS  # Text thickness (2 pixels)
    )

    # ========================================================================
    # DRAW CURRENT MODE INDICATOR
    # ========================================================================
    # Display the current gesture mode being detected

    # Choose color based on mode
    # Cyan for default CURSOR mode, Orange for active gesture modes
    if gesture_mode == MODE_CURSOR:
        mode_color = COLOR_CYAN  # Cyan for default/idle mode
    else:
        mode_color = COLOR_ORANGE  # Orange for active gestures

    # Format mode text
    mode_text = f"Mode: {gesture_mode}"

    # Draw the mode text below the FPS
    cv2.putText(
        frame,  # Image to draw on
        mode_text,  # Text to display
        (10, 60),  # Position (x=10, y=60 from top-left)
        cv2.FONT_HERSHEY_SIMPLEX,  # Font type
        FONT_SCALE_LARGE,  # Font size (0.7 scale)
        mode_color,  # Color (cyan or orange)
        FONT_THICKNESS  # Text thickness (2 pixels)
    )

    # ========================================================================
    # DRAW KEYBOARD SHORTCUTS REMINDER
    # ========================================================================
    # Display helpful keyboard shortcuts at the bottom of the info panel

    # Create the shortcuts text
    shortcuts_text = "Press 'Q' to quit | 'H' for help"

    # Draw the shortcuts text
    cv2.putText(
        frame,  # Image to draw on
        shortcuts_text,  # Text to display
        (10, 90),  # Position (x=10, y=90 from top-left)
        cv2.FONT_HERSHEY_SIMPLEX,  # Font type
        FONT_SCALE_SMALL,  # Smaller font size (0.5 scale)
        COLOR_WHITE,  # White color for instructions
        1  # Thinner text (1 pixel thickness)
    )

    # Note: Frame is modified in-place, no return needed


# ============================================================================
# HELP OVERLAY DRAWING FUNCTION
# ============================================================================

def show_help_overlay(frame, frame_width, frame_height):
    """
    Display a full-screen help overlay with gesture instructions.

    This overlay shows all available gestures and how to perform them.
    It's toggled on/off by pressing the 'H' key.

    Parameters:
        frame (numpy.ndarray): The video frame to draw on (modified in-place)
        frame_width (int): Width of the frame in pixels
        frame_height (int): Height of the frame in pixels

    Returns:
        None (frame is modified in-place)

    Visual Design:
        - Dark semi-transparent background (80% opacity)
        - Cyan headers for section titles
        - White text for instructions
        - Centered and well-spaced for readability
    """
    # ========================================================================
    # CREATE DARK OVERLAY BACKGROUND
    # ========================================================================
    # Create a copy of the frame for the overlay
    overlay = frame.copy()

    # Draw a filled black rectangle covering the entire frame
    cv2.rectangle(
        overlay,  # Draw on the overlay
        (0, 0),  # Top-left corner
        (frame_width, frame_height),  # Bottom-right corner (full frame)
        COLOR_BLACK,  # Black color
        -1  # Filled rectangle
    )

    # Blend the overlay with original frame for transparency
    # 80% overlay makes it darker, ensuring text is readable
    cv2.addWeighted(
        overlay, 0.8,  # Dark overlay with 80% weight
        frame, 0.2,  # Original frame with 20% weight (barely visible)
        0,  # No gamma adjustment
        frame  # Write back to original frame
    )

    # ========================================================================
    # DEFINE HELP TEXT CONTENT
    # ========================================================================
    # Create a list of text lines to display
    # Empty strings create spacing between sections
    help_text = [
        "GESTURE CONTROLS:",  # Header (will be cyan)
        "",  # Empty line for spacing
        "Move Cursor: Point with index finger",  # Instruction
        "Left Click: Pinch thumb + index finger",
        "Right Click: Pinch thumb + middle finger",
        "Drag & Drop: Hold left click pinch while moving",
        "Scroll: Extend all 5 fingers and move up/down",
        "",  # Empty line for spacing
        "Press 'H' to close help"  # Instruction to close
    ]

    # ========================================================================
    # DRAW HELP TEXT LINE BY LINE
    # ========================================================================
    # Starting y-position for text (80 pixels from top)
    y_offset = 80

    # Line spacing (40 pixels between each line)
    line_spacing = 40

    # Iterate through each line with its index
    for i, text in enumerate(help_text):
        # Skip empty lines (but they still add to spacing)
        if text == "":
            continue

        # Determine text color based on whether it's a header
        # Headers end with ":" character
        if text.endswith(":"):
            color = COLOR_CYAN  # Cyan for headers
            thickness = 2  # Thicker (bold) for headers
        else:
            color = COLOR_WHITE  # White for regular text
            thickness = 1  # Normal thickness for instructions

        # Calculate y-position for this line
        y_position = y_offset + (i * line_spacing)

        # Draw the text line
        cv2.putText(
            frame,  # Image to draw on
            text,  # Text content
            (50, y_position),  # Position (x=50 pixels from left, y=calculated)
            cv2.FONT_HERSHEY_SIMPLEX,  # Font type
            FONT_SCALE_LARGE,  # Font size (0.7 scale)
            color,  # Color (cyan for headers, white for text)
            thickness  # Thickness (2 for headers, 1 for text)
        )

    # Note: Frame is modified in-place, no return needed


# ============================================================================
# HAND DETECTION STATUS INDICATOR
# ============================================================================

def draw_hand_detected_indicator(frame, frame_width):
    """
    Draw "Hand Detected" indicator in the top-right corner.

    This provides immediate visual feedback that the system is tracking a hand.

    Parameters:
        frame (numpy.ndarray): The video frame to draw on
        frame_width (int): Width of the frame in pixels

    Returns:
        None (frame is modified in-place)
    """
    # Calculate x-position for right-aligned text
    # Subtract 200 pixels from right edge for text placement
    x_position = frame_width - 200

    # Draw the "Hand Detected" text
    cv2.putText(
        frame,  # Image to draw on
        "Hand Detected",  # Text to display
        (x_position, 30),  # Position (top-right area)
        cv2.FONT_HERSHEY_SIMPLEX,  # Font type
        FONT_SCALE_LARGE,  # Font size
        COLOR_GREEN,  # Green color (active/success)
        FONT_THICKNESS  # Text thickness
    )


# ============================================================================
# GESTURE INDICATOR DRAWING
# ============================================================================

def draw_gesture_indicator(frame, gesture_mode, frame_width, frame_height):
    """
    Draw large gesture indicators for active modes (SCROLLING, DRAGGING, CLICKING).

    These are prominent visual indicators that appear in the center of the screen
    to clearly show when a special gesture is being performed.

    Parameters:
        frame (numpy.ndarray): The video frame to draw on
        gesture_mode (str): Current gesture mode
        frame_width (int): Width of frame
        frame_height (int): Height of frame

    Returns:
        None (frame is modified in-place)
    """
    # Check if we're in scroll mode
    if gesture_mode == MODE_SCROLL:
        # Draw "SCROLLING" text in the top-center of the frame
        cv2.putText(
            frame,
            "SCROLLING",  # Text to display
            (frame_width // 2 - 80, 50),  # Centered horizontally, near top
            cv2.FONT_HERSHEY_SIMPLEX,
            1,  # Larger font size for visibility
            COLOR_YELLOW,  # Yellow for scroll mode
            2  # Thick text
        )

    # Check if we're in left click mode
    elif gesture_mode == MODE_LEFT_CLICK:
        # Draw "CLICKING" text in the top-center
        cv2.putText(
            frame,
            "CLICKING",
            (frame_width // 2 - 80, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            COLOR_RED,  # Red for left click
            2
        )


# ============================================================================
# DRAG MODE INDICATOR
# ============================================================================

def draw_drag_indicator(frame, frame_width, frame_height):
    """
    Draw "DRAGGING" indicator at the bottom-center when in drag mode.

    Parameters:
        frame (numpy.ndarray): The video frame to draw on
        frame_width (int): Width of frame
        frame_height (int): Height of frame

    Returns:
        None (frame is modified in-place)
    """
    # Draw "DRAGGING" text near the bottom-center
    cv2.putText(
        frame,
        "DRAGGING",
        (frame_width // 2 - 80, frame_height - 50),  # Bottom-center
        cv2.FONT_HERSHEY_SIMPLEX,
        1,  # Large font
        COLOR_ORANGE,  # Orange for drag mode
        2  # Thick text
    )


# ============================================================================
# MODULE INITIALIZATION COMPLETE
# ============================================================================

print("[GESTURE_UTILS] ✓ All utility functions loaded successfully")
print("[GESTURE_UTILS] ✓ Functions available:")
print("[GESTURE_UTILS]   - get_distance()")
print("[GESTURE_UTILS]   - count_extended_fingers()")
print("[GESTURE_UTILS]   - draw_info_panel()")
print("[GESTURE_UTILS]   - show_help_overlay()")
print("[GESTURE_UTILS]   - draw_hand_detected_indicator()")
print("[GESTURE_UTILS]   - draw_gesture_indicator()")
print("[GESTURE_UTILS]   - draw_drag_indicator()")
print("=" * 70)