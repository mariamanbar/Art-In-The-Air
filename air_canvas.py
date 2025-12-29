import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Canvas
canvas = None
prev_x, prev_y = 0, 0

# Colors (BGR)
colors = [
    (255, 0, 255),    # Purple
    (255, 0, 0),      # Blue
    (0, 255, 0),      # Green
    (0, 255, 255),    # Yellow
    (0, 0, 0)         # Eraser
]
color_names = ["PURPLE", "BLUE", "GREEN", "YELLOW", "ERASER"]
current_color = colors[0]

def fingers_up(hand):
    fingers = []
    # Thumb is ignored
    fingers.append(hand.landmark[8].y < hand.landmark[6].y)    # Index
    fingers.append(hand.landmark[12].y < hand.landmark[10].y)  # Middle
    return fingers

def draw_palette(img, active_color):
    h, w, _ = img.shape
    
    # Draw a grey toolbar background
    #cv2.rectangle(img, (0, 0), (w, 70), (50, 50, 50), -1)

    box_w = w // len(colors)
    
    # Draw the colores box
    for i, col in enumerate(colors):
        x1 = i * box_w + 5 # Added minimal padding
        x2 = (i + 1) * box_w - 5
        y1 = 10
        y2 = 60
        
        # Draw the color box
        cv2.rectangle(img, (x1, y1), (x2, y2), col, -1)
        
        # 2. Logic to change text color: White text for Eraser, Black for others
        text_color = (255, 255, 255) if col == (0, 0, 0) else (50, 50, 50)
        
        # Draw the text centered
        cv2.putText(img, color_names[i], (x1 + 10, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
        
        # 3. Draw a highlight border if this is the ACTIVE color
        if col == active_color:
            cv2.rectangle(img, (x1-3, y1-3), (x2+3, y2+3), (255, 255, 255), 3)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # Convert to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    mode = "HOVER" # Default mode

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            
            # Draw landmarks (optional: comment out if you want a cleaner look)
            index_up, middle_up = fingers_up(hand)

            x = int(hand.landmark[8].x * w)
            y = int(hand.landmark[8].y * h)

            # --- SELECTION MODE (Index + Middle Up) ---
            if index_up and middle_up:
                mode = "SELECT"
                prev_x, prev_y = 0, 0
                
                # Visual Indicator on fingers
                cv2.circle(frame, (x, y), 20, (255, 255, 255), 2) 

                if y < 70: # Check if in toolbar area
                    box_w = w // len(colors)
                    idx = x // box_w
                    if idx < len(colors):
                        current_color = colors[idx]

            # --- DRAW MODE (Only Index Up) ---
            elif index_up and not middle_up:
                mode = "DRAW"
                
                # Visual Indicator: Show the color on the fingertip
                cv2.circle(frame, (x, y), 10, current_color, -1)

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y

                thickness = 50 if current_color == (0, 0, 0) else 8
                cv2.line(canvas, (prev_x, prev_y), (x, y), current_color, thickness)
                prev_x, prev_y = x, y

            else:
                prev_x, prev_y = 0, 0

    else:
        prev_x, prev_y = 0, 0

    # --- MERGING LAYERS ---
    
    # 1. Prepare the canvas
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    
    # 2. Add canvas to frame
    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    # 3. Draw the User Interface (Palette) on top
    draw_palette(frame, current_color)

    # 4. Draw the Bottom Info Bar (Semi-Transparent)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - 80), (w, h), (0, 0, 0), -1) # Dark bar at bottom
    alpha = 0.6 # Transparency factor
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    # 5. Add Text
    cv2.putText(frame, f"Mode: {mode}", (20, h - 50), 
                cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
    
    cv2.putText(frame, "Index: Draw | 2 Fingers: Select | C: Clear | Q: Quit", 
                (20, h - 20), cv2.FONT_HERSHEY_DUPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow("Air Canvas", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()