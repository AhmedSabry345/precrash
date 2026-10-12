import math
import threading
import time
from collections import deque

import cv2
import mediapipe as mp
import numpy as np

try:
    import winsound  # Windows only; other systems fall back to terminal bell
except ImportError:
    winsound = None

# PreCrash AI - Driver Eye Monitoring Prototype (HUD edition)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

EAR_THRESHOLD = 0.20
ALERT_SECONDS = 1.5

# Display settings
UI_W, UI_H = 1280, 720
EAR_MAX = 0.45          # gauge full-scale value
GRAPH_SAMPLES = 180     # points kept in the EAR trend graph
PERCLOS_WINDOW = 30     # seconds used for the fatigue index

# Colors (BGR)
WHITE = (240, 240, 240)
GRAY = (150, 150, 150)
DARK = (28, 22, 18)
CYAN = (255, 210, 60)
GREEN = (120, 230, 100)
AMBER = (0, 180, 255)
RED = (70, 70, 255)


# ----------------------------------------------------------------------------
# Detection logic
# ----------------------------------------------------------------------------

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def eye_points_px(landmarks, eye_indices, width, height):
    return [
        (int(landmarks[i].x * width), int(landmarks[i].y * height))
        for i in eye_indices
    ]


def eye_ratio(points):
    vertical_1 = distance(points[1], points[5])
    vertical_2 = distance(points[2], points[4])
    horizontal = distance(points[0], points[3])

    if horizontal == 0:
        return 0

    return (vertical_1 + vertical_2) / (2 * horizontal)


# ----------------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------------

def blend_rect(img, p1, p2, color, alpha):
    x1, y1 = max(0, p1[0]), max(0, p1[1])
    x2, y2 = min(img.shape[1], p2[0]), min(img.shape[0], p2[1])
    roi = img[y1:y2, x1:x2]
    if roi.size == 0:
        return
    overlay = np.full_like(roi, color)
    img[y1:y2, x1:x2] = cv2.addWeighted(overlay, alpha, roi, 1 - alpha, 0)


def text(img, s, org, scale=0.55, color=WHITE, thick=1, align="left",
         font=cv2.FONT_HERSHEY_SIMPLEX):
    (w, _), _ = cv2.getTextSize(s, font, scale, thick)
    x, y = org
    if align == "center":
        x -= w // 2
    elif align == "right":
        x -= w
    cv2.putText(img, s, (x + 1, y + 1), font, scale, (0, 0, 0), thick + 1, cv2.LINE_AA)
    cv2.putText(img, s, (x, y), font, scale, color, thick, cv2.LINE_AA)


def corner_brackets(img, x1, y1, x2, y2, color, length=28, thick=3):
    for x, y, dx, dy in ((x1, y1, 1, 1), (x2, y1, -1, 1),
                         (x1, y2, 1, -1), (x2, y2, -1, -1)):
        cv2.line(img, (x, y), (x + dx * length, y), color, thick, cv2.LINE_AA)
        cv2.line(img, (x, y), (x, y + dy * length), color, thick, cv2.LINE_AA)


def panel(img, x1, y1, x2, y2, accent=CYAN):
    blend_rect(img, (x1, y1), (x2, y2), DARK, 0.62)
    corner_brackets(img, x1, y1, x2, y2, accent, length=14, thick=2)


def draw_gauge(img, center, radius, value, vmax, threshold, color):
    start, sweep = 135, 270
    cv2.ellipse(img, center, (radius, radius), 0, start, start + sweep,
                (75, 65, 55), 10, cv2.LINE_AA)

    frac = max(0.0, min(1.0, value / vmax))
    if frac > 0.01:
        cv2.ellipse(img, center, (radius, radius), 0, start,
                    start + sweep * frac, color, 10, cv2.LINE_AA)

    # Threshold tick mark
    ang = math.radians(start + sweep * threshold / vmax)
    p1 = (int(center[0] + (radius - 14) * math.cos(ang)),
          int(center[1] + (radius - 14) * math.sin(ang)))
    p2 = (int(center[0] + (radius + 14) * math.cos(ang)),
          int(center[1] + (radius + 14) * math.sin(ang)))
    cv2.line(img, p1, p2, AMBER, 2, cv2.LINE_AA)


def draw_bar(img, x, y, w, h, frac, color):
    cv2.rectangle(img, (x, y), (x + w, y + h), (75, 65, 55), -1)
    fill = int(w * max(0.0, min(1.0, frac)))
    if fill > 0:
        cv2.rectangle(img, (x, y), (x + fill, y + h), color, -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), GRAY, 1)


def draw_graph(img, x1, y1, x2, y2, values, vmax, threshold, color):
    cv2.rectangle(img, (x1, y1), (x2, y2), (60, 52, 45), 1)

    ty = int(y2 - (threshold / vmax) * (y2 - y1))
    for x in range(x1, x2, 10):
        cv2.line(img, (x, ty), (min(x + 5, x2), ty), AMBER, 1, cv2.LINE_AA)

    if len(values) < 2:
        return

    step = (x2 - x1) / (GRAPH_SAMPLES - 1)
    offset = GRAPH_SAMPLES - len(values)
    pts = []
    for i, v in enumerate(values):
        px = int(x1 + (offset + i) * step)
        py = int(y2 - max(0.0, min(1.0, v / vmax)) * (y2 - y1))
        pts.append((px, py))
    cv2.polylines(img, [np.array(pts, dtype=np.int32)], False, color, 2, cv2.LINE_AA)


def stat_row(img, label, value, x1, x2, y, color=WHITE):
    text(img, label, (x1, y), 0.45, GRAY)
    text(img, value, (x2, y), 0.62, color, 2, align="right")
    cv2.line(img, (x1, y + 10), (x2, y + 10), (60, 52, 45), 1)


def beep():
    if winsound:
        threading.Thread(target=winsound.Beep, args=(1800, 250), daemon=True).start()
    else:
        print("\a", end="", flush=True)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, UI_W)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, UI_H)

    if not camera.isOpened():
        print("ERROR: Camera could not be opened.")
        return

    closed_since = None
    session_start = time.time()
    blink_total = 0
    blink_times = deque()
    closed_log = deque()          # (timestamp, eyes_closed) for the fatigue index
    ear_history = deque(maxlen=GRAPH_SAMPLES)
    last_beep = 0.0
    fps = 0.0
    prev_time = time.time()

    cv2.namedWindow("PreCrash AI - Driver Monitoring", cv2.WINDOW_NORMAL)

    with mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while True:
            success, frame = camera.read()

            if not success:
                print("ERROR: Could not read camera frame.")
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (UI_W, UI_H))
            height, width = frame.shape[:2]
            now = time.time()

            fps = 0.9 * fps + 0.1 * (1.0 / max(now - prev_time, 1e-6))
            prev_time = now

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(rgb)

            state = "NO_FACE"
            ear = 0.0
            closed_for = 0.0
            face_box = None
            eye_pts = []

            if result.multi_face_landmarks:
                landmarks = result.multi_face_landmarks[0].landmark

                left_pts = eye_points_px(landmarks, LEFT_EYE, width, height)
                right_pts = eye_points_px(landmarks, RIGHT_EYE, width, height)
                eye_pts = [left_pts, right_pts]

                ear = (eye_ratio(left_pts) + eye_ratio(right_pts)) / 2
                ear_history.append(ear)

                xs = [l.x for l in landmarks]
                ys = [l.y for l in landmarks]
                pad = 20
                face_box = (int(min(xs) * width) - pad, int(min(ys) * height) - pad,
                            int(max(xs) * width) + pad, int(max(ys) * height) + pad)

                if ear < EAR_THRESHOLD:
                    if closed_since is None:
                        closed_since = now
                    closed_for = now - closed_since
                    state = "ALERT" if closed_for >= ALERT_SECONDS else "CLOSING"
                else:
                    if closed_since is not None:
                        duration = now - closed_since
                        if 0.05 <= duration < ALERT_SECONDS:
                            blink_total += 1
                            blink_times.append(now)
                    closed_since = None
                    state = "ATTENTIVE"

                closed_log.append((now, ear < EAR_THRESHOLD))
            else:
                closed_since = None

            # Rolling windows
            while blink_times and now - blink_times[0] > 60:
                blink_times.popleft()
            while closed_log and now - closed_log[0][0] > PERCLOS_WINDOW:
                closed_log.popleft()

            if closed_log:
                perclos = sum(1 for _, c in closed_log if c) / len(closed_log)
            else:
                perclos = 0.0
            fatigue = min(1.0, perclos * 3)

            # UI

            colors = {"NO_FACE": GRAY, "ATTENTIVE": GREEN,
                      "CLOSING": AMBER, "ALERT": RED}
            labels = {"NO_FACE": "SEARCHING FOR DRIVER",
                      "ATTENTIVE": "DRIVER ATTENTIVE",
                      "CLOSING": "EYES CLOSING",
                      "ALERT": "DROWSINESS DETECTED"}
            color = colors[state]




            # Face tracking box + eye outlines
            if face_box:
                corner_brackets(frame, *face_box, color)
                for pts in eye_pts:
                    cv2.polylines(frame, [np.array(pts, dtype=np.int32)],
                                  True, color, 2, cv2.LINE_AA)
                    for p in pts:
                        cv2.circle(frame, p, 2, WHITE, -1, cv2.LINE_AA)


            else:
                cx, cy = width // 2, height // 2
                corner_brackets(frame, cx - 150, cy - 190, cx + 150, cy + 190,
                                GRAY, 40, 2)
                text(frame, "ALIGN FACE WITH CAMERA", (cx, cy + 230), 0.6,
                     GRAY, align="center")
                


            if state == "ALERT":
                pulse = 0.5 + 0.5 * math.sin(now * 9)
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (width - 1, height - 1), RED, 36)
                frame = cv2.addWeighted(overlay, 0.25 + 0.45 * pulse,
                                        frame, 0.75 - 0.45 * pulse, 0)
                if now - last_beep > 0.6:
                    beep()
                    last_beep = now

            # Bars
            blend_rect(frame, (0, 0), (width, 58), DARK, 0.75)
            cv2.line(frame, (0, 58), (width, 58), CYAN, 1, cv2.LINE_AA)
            cv2.circle(frame, (36, 29), 8, RED if state == "ALERT" else CYAN, -1, cv2.LINE_AA)
            text(frame, "PRECRASH AI", (56, 37), 0.9, WHITE, 2)
            text(frame, "DRIVER MONITORING SYSTEM", (260, 36), 0.45, GRAY)
            text(frame, time.strftime("%H:%M:%S"), (width - 150, 36), 0.6, WHITE, 1, "right")
            text(frame, f"{fps:4.0f} FPS", (width - 30, 36), 0.6, CYAN, 1, "right")



            lx1, ly1, lx2, ly2 = 20, 80, 300, 600
            panel(frame, lx1, ly1, lx2, ly2)
            text(frame, "EYE ASPECT RATIO", ((lx1 + lx2) // 2, ly1 + 28), 0.5, CYAN, 1, "center")
            draw_gauge(frame, (160, 205), 70, ear, EAR_MAX, EAR_THRESHOLD, color)
            text(frame, f"{ear:.2f}" if face_box else "--", (160, 215), 1.1, color, 2, "center")
            text(frame, f"ALERT BELOW {EAR_THRESHOLD:.2f}", (160, 300), 0.4, GRAY, 1, "center")



            bpm = len(blink_times)
            session = int(now - session_start)
            stat_row(frame, "BLINKS / MIN", str(bpm), 40, 280, 345)
            stat_row(frame, "TOTAL BLINKS", str(blink_total), 40, 280, 385)
            stat_row(frame, "EYES CLOSED", f"{closed_for:.1f}s",
                     40, 280, 425, color if closed_for > 0 else WHITE)
            stat_row(frame, "SESSION", f"{session // 60:02d}:{session % 60:02d}", 40, 280, 465)

            fat_color = GREEN if fatigue < 0.35 else AMBER if fatigue < 0.7 else RED
            text(frame, "FATIGUE INDEX", (40, 515), 0.45, GRAY)
            text(frame, f"{int(fatigue * 100)}%", (280, 515), 0.55, fat_color, 2, "right")
            draw_bar(frame, 40, 527, 240, 14, fatigue, fat_color)
            text(frame, f"{PERCLOS_WINDOW}s rolling window", (40, 570), 0.4, GRAY)


            rx1, ry1, rx2, ry2 = width - 300, 80, width - 20, 260
            panel(frame, rx1, ry1, rx2, ry2)
            text(frame, "EAR TREND", (rx1 + 18, ry1 + 28), 0.5, CYAN)
            draw_graph(frame, rx1 + 18, ry1 + 45, rx2 - 18, ry2 - 18,
                       ear_history, EAR_MAX, EAR_THRESHOLD, color)


            if state == "ALERT":
                pulse = 0.5 + 0.5 * math.sin(now * 9)
                blend_rect(frame, (width // 2 - 260, 90), (width // 2 + 260, 190), RED,
                           0.55 + 0.3 * pulse)
                text(frame, "WAKE UP!", (width // 2, 145), 1.7, WHITE, 4, "center")
                text(frame, f"EYES CLOSED FOR {closed_for:.1f}s",
                     (width // 2, 178), 0.55, WHITE, 1, "center")

            # Bottom status banner
            bx1, bx2 = width // 2 - 220, width // 2 + 220
            blend_rect(frame, (bx1, height - 80), (bx2, height - 28), color, 0.35)
            cv2.rectangle(frame, (bx1, height - 80), (bx2, height - 28), color, 2, cv2.LINE_AA)
            text(frame, labels[state], (width // 2, height - 46), 0.8, WHITE, 2, "center")

            text(frame, "Q  quit    R  reset stats", (30, height - 20), 0.42, GRAY)

            cv2.imshow("PreCrash AI - Driver Monitoring", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("r"):
                blink_total = 0
                blink_times.clear()
                closed_log.clear()
                ear_history.clear()
                session_start = time.time()

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
