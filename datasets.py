import os
import pickle

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []
for dir_ in os.listdir(DATA_DIR):
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        data_aux = []

        x_ = []
        y_ = []

        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            for id, landmark in enumerate(hand_landmarks.landmark):
                x = landmark.x
                y = landmark.y
                x_.append(x)
                y_.append(y)

    # Chỉ xét bàn tay đầu tiên.
            x_min = min(x_)
            y_min = min(y_)

            for id, landmark in enumerate(hand_landmarks.landmark):
                x = landmark.x - x_min
                y = landmark.y - y_min
                data_aux.append(x)
                data_aux.append(y)

    # Thêm data_aux vào data sau khi đã xác định nhãn.
            data.append(data_aux)
            labels.append(dir_)
        
f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
