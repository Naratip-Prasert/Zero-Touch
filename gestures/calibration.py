import time
import numpy as np


class GestureCalibration:
    def __init__(self, duration=3.0):
        self.duration = duration
        self.start_time = None
        self.hand_sizes = []
        self.finished = False
        self.average_hand_size = None

    def update(self, handLms):
        if self.finished:
            return True

        if self.start_time is None:
            self.start_time = time.time()

        lm = handLms.landmark
        wrist = lm[0]
        middle_base = lm[9]

        hand_size = np.hypot(
            wrist.x - middle_base.x,
            wrist.y - middle_base.y
        )

        self.hand_sizes.append(hand_size)

        if time.time() - self.start_time >= self.duration:
            self.average_hand_size = sum(self.hand_sizes) / len(self.hand_sizes)
            self.finished = True
            print(f"Calibration complete: {self.average_hand_size:.4f}")
            return True

        return False

    def get_progress(self):
        if self.start_time is None:
            return 0

        progress = (time.time() - self.start_time) / self.duration
        return min(1, progress)