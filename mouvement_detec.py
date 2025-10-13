import cv2
import mediapipe as mp
import keyboard
import time
import ctypes, sys

# Vérification des droits administrateur
def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not check_admin():
    print("⚠️ Le script n'est pas lancé en mode administrateur !")
    input("Appuie sur Entrée pour fermer...")
    sys.exit()

# Initialiser MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)

# Zones d’intérêt pour les touches WSAD
zones = {
    "w": (220, 50, 420, 150),    # haut (W)
    "s": (220, 330, 420, 430),   # bas (S)
    "d": (50, 190, 150, 390),    # gauche (A)
    "a": (490, 190, 590, 390)    # droite (D)
}



# Dictionnaire pour gérer les temps de dernière activation
last_press_time = {zone: 0 for zone in zones}
cooldown = 0.25  # secondes entre deux pressions

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Coordonnées des mains
        left_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        height, width, _ = frame.shape
        left_hand_x, left_hand_y = int(left_hand.x * width), int(left_hand.y * height)
        right_hand_x, right_hand_y = int(right_hand.x * width), int(right_hand.y * height)

        # Vérifier les zones
        for key, (x_min, y_min, x_max, y_max) in zones.items():
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            current_time = time.time()

            # Main gauche
            if x_min < left_hand_x < x_max and y_min < left_hand_y < y_max:
                cv2.putText(frame, f"Main gauche -> {key}", (left_hand_x, left_hand_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                if current_time - last_press_time[key] > cooldown:
                    keyboard.press_and_release(key)
                    print(f"[{key}] pressé (main gauche)")
                    last_press_time[key] = current_time

            # Main droite
            if x_min < right_hand_x < x_max and y_min < right_hand_y < y_max:
                cv2.putText(frame, f"Main droite -> {key}", (right_hand_x, right_hand_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                if current_time - last_press_time[key] > cooldown:
                    keyboard.press_and_release(key)
                    print(f"[{key}] pressé (main droite)")
                    last_press_time[key] = current_time

    cv2.imshow('MediaPipe Pose', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
