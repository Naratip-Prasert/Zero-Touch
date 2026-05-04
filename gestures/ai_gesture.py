import joblib

model = joblib.load("models/gesture_model.pkl")

def predict_gesture(handLms):
    data = []

    for lm in handLms.landmark:
        data.extend([lm.x, lm.y])

    return model.predict([data])[0]