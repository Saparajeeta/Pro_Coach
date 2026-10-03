import time

import cv2
import numpy as np

from audio_feedback import speak_feedback
from utils import draw_text, find_angle, get_landmark_features


class ProcessFrameFootball:
    def __init__(self, thresholds=None, flip_frame=False):
        self.thresholds = thresholds or {
            "KICK_KNEE_ANGLE": 90,
            "TRUNK_TILT": 25,
            "PLANT_FOOT_SPACING": 60,
            "KNEE_SNAP": 140,
            "CNT_FRAME_THRESH": 25,
        }
        self.flip_frame = flip_frame
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.linetype = cv2.LINE_AA
        self.COLORS = {
            "blue": (0, 127, 255),
            "red": (255, 50, 50),
            "green": (0, 255, 127),
            "white": (255, 255, 255),
            "yellow": (255, 255, 0),
            "cyan": (0, 255, 255),
            "aqua": (192, 220, 205),
            "rose": (255, 102, 204),
        }
        self.dict_features = {}
        self.left_features = {
            "shoulder": 11, "elbow": 13, "wrist": 15, "hip": 23, "knee": 25, "ankle": 27, "foot": 31,
        }
        self.right_features = {
            "shoulder": 12, "elbow": 14, "wrist": 16, "hip": 24, "knee": 26, "ankle": 28, "foot": 32,
        }
        self.dict_features["left"] = self.left_features
        self.dict_features["right"] = self.right_features
        self.state_tracker = {
            "state_seq": [],
            "DISPLAY_TEXT": np.full((4,), False),
            "COUNT_FRAMES": np.zeros((4,), dtype=np.int64),
            "INCORRECT_POSTURE": False,
            "prev_state": None,
            "curr_state": None,
            "FOOTBALL_COUNT": 0,
            "IMPROPER_KICK": 0,
            "start_inactive_time": time.perf_counter(),
            "INACTIVE_TIME": 0.0,
        }
        self.FEEDBACK_ID_MAP = {
            0: ("WIDE PLANT FOOT", 175, (0, 153, 255)),
            1: ("KEEP TRUNK OVER BALL", 140, (0, 153, 255)),
            2: ("LOAD KICKING LEG", 105, (255, 80, 80)),
            3: ("SNAP KNEE THROUGH", 70, (255, 80, 80)),
        }

    def _choose_kicking_leg(self, left_hip, right_hip, left_knee, right_knee):
        left_score = abs(left_hip[0] - left_knee[0]) + abs(left_hip[1] - left_knee[1])
        right_score = abs(right_hip[0] - right_knee[0]) + abs(right_hip[1] - right_knee[1])
        return "left" if left_score > right_score else "right"

    def _get_state(self, knee_snap, plant_spacing, trunk_angle):
        if knee_snap < 110 and plant_spacing > 40 and trunk_angle < 20:
            return "s1"
        if knee_snap > 150 and plant_spacing > 50 and trunk_angle < 25:
            return "s2"
        return "s0"

    def _update_state_sequence(self, state):
        if state == "s1":
            if "s2" not in self.state_tracker["state_seq"]:
                self.state_tracker["state_seq"].append(state)
        elif state == "s2":
            if "s1" in self.state_tracker["state_seq"] and "s2" not in self.state_tracker["state_seq"]:
                self.state_tracker["state_seq"].append(state)

    def _show_feedback(self, frame, count_mask, dict_maps):
        for idx in np.where(count_mask)[0]:
            draw_text(
                frame,
                dict_maps[idx][0],
                pos=(30, dict_maps[idx][1]),
                text_color=(255, 255, 230),
                font_scale=0.6,
                text_color_bg=dict_maps[idx][2],
            )
        return frame

    def process(self, frame: np.ndarray, pose):
        play_sound = None
        frame_height, frame_width, _ = frame.shape
        keypoints = pose.process(frame)

        if keypoints.pose_landmarks:
            lm = keypoints.pose_landmarks.landmark
            left_shoulder, left_elbow, left_wrist, left_hip, left_knee, left_ankle, left_foot = get_landmark_features(lm, self.dict_features, "left", frame_width, frame_height)
            right_shoulder, right_elbow, right_wrist, right_hip, right_knee, right_ankle, right_foot = get_landmark_features(lm, self.dict_features, "right", frame_width, frame_height)
            kicking_leg = self._choose_kicking_leg(left_hip, right_hip, left_knee, right_knee)

            if kicking_leg == "left":
                kick_hip, kick_knee, kick_ankle = left_hip, left_knee, left_ankle
                plant_hip, plant_knee, plant_ankle = right_hip, right_knee, right_ankle
                plant_foot = right_foot
            else:
                kick_hip, kick_knee, kick_ankle = right_hip, right_knee, right_ankle
                plant_hip, plant_knee, plant_ankle = left_hip, left_knee, left_ankle
                plant_foot = left_foot

            knee_angle = find_angle(kick_hip, kick_knee, ref_pt=kick_ankle)
            trunk_angle = find_angle(np.array([left_shoulder[0], left_shoulder[1] - 40]), left_shoulder, ref_pt=np.mean([left_hip, right_hip], axis=0))
            plant_spacing = abs(plant_foot[0] - (kick_foot if 'kick_foot' in locals() else plant_foot)[0])

            kick_foot = left_foot if kicking_leg == "left" else right_foot
            plant_spacing = abs(kick_foot[0] - plant_foot[0])

            cv2.line(frame, kick_hip, kick_knee, self.COLORS["aqua"], 4, lineType=self.linetype)
            cv2.line(frame, kick_knee, kick_ankle, self.COLORS["aqua"], 4, lineType=self.linetype)
            cv2.line(frame, plant_hip, plant_knee, self.COLORS["aqua"], 4, lineType=self.linetype)
            cv2.line(frame, plant_knee, plant_ankle, self.COLORS["aqua"], 4, lineType=self.linetype)
            cv2.circle(frame, kick_hip, 7, self.COLORS["rose"], -1)
            cv2.circle(frame, kick_knee, 7, self.COLORS["rose"], -1)
            cv2.circle(frame, kick_ankle, 7, self.COLORS["rose"], -1)
            cv2.circle(frame, plant_foot, 7, self.COLORS["yellow"], -1)

            state = self._get_state(int(knee_angle), int(plant_spacing), int(trunk_angle))
            self.state_tracker["curr_state"] = state
            self._update_state_sequence(state)

            if state == "s2" and self.state_tracker["state_seq"] == ["s1", "s2"]:
                self.state_tracker["FOOTBALL_COUNT"] += 1
                play_sound = str(self.state_tracker["FOOTBALL_COUNT"])
                if self.state_tracker["INCORRECT_POSTURE"]:
                    self.state_tracker["IMPROPER_KICK"] += 1
                self.state_tracker["state_seq"] = []
                self.state_tracker["INCORRECT_POSTURE"] = False

            if plant_spacing < self.thresholds["PLANT_FOOT_SPACING"]:
                self.state_tracker["DISPLAY_TEXT"][0] = True
                speak_feedback("football_0", self.FEEDBACK_ID_MAP[0][0].capitalize())
                self.state_tracker["INCORRECT_POSTURE"] = True
            if trunk_angle > self.thresholds["TRUNK_TILT"]:
                self.state_tracker["DISPLAY_TEXT"][1] = True
                speak_feedback("football_1", self.FEEDBACK_ID_MAP[1][0].capitalize())
                self.state_tracker["INCORRECT_POSTURE"] = True
            if knee_angle > 120:
                self.state_tracker["DISPLAY_TEXT"][2] = True
                speak_feedback("football_2", self.FEEDBACK_ID_MAP[2][0].capitalize())
                self.state_tracker["INCORRECT_POSTURE"] = True
            if knee_angle > self.thresholds["KNEE_SNAP"]:
                self.state_tracker["DISPLAY_TEXT"][3] = True
                speak_feedback("football_3", self.FEEDBACK_ID_MAP[3][0].capitalize())
                self.state_tracker["INCORRECT_POSTURE"] = True

            if self.state_tracker["curr_state"] == self.state_tracker["prev_state"]:
                end_time = time.perf_counter()
                self.state_tracker["INACTIVE_TIME"] += end_time - self.state_tracker["start_inactive_time"]
                self.state_tracker["start_inactive_time"] = end_time
                if self.state_tracker["INACTIVE_TIME"] >= 12.0:
                    self.state_tracker["FOOTBALL_COUNT"] = 0
                    self.state_tracker["IMPROPER_KICK"] = 0
            else:
                self.state_tracker["start_inactive_time"] = time.perf_counter()
                self.state_tracker["INACTIVE_TIME"] = 0.0

            if self.flip_frame:
                frame = cv2.flip(frame, 1)

            frame = self._show_feedback(frame, self.state_tracker["DISPLAY_TEXT"], self.FEEDBACK_ID_MAP)
            cv2.putText(frame, f"Rep: {self.state_tracker['FOOTBALL_COUNT']}", (30, 30), self.font, 0.8, self.COLORS["green"], 2, cv2.LINE_AA)
            draw_text(frame, f"Knee snap: {int(knee_angle)}°", pos=(int(frame_width * 0.68), 30), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(18, 185, 0))
            draw_text(frame, f"Plant gap: {int(plant_spacing)} px", pos=(int(frame_width * 0.68), 80), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(0, 120, 180))

            self.state_tracker["DISPLAY_TEXT"] = np.full((4,), False)
            self.state_tracker["prev_state"] = self.state_tracker["curr_state"]
        else:
            if self.flip_frame:
                frame = cv2.flip(frame, 1)
            draw_text(frame, f"Rep: {self.state_tracker['FOOTBALL_COUNT']}", pos=(30, 30), text_color=(255, 255, 230), font_scale=0.8, text_color_bg=(18, 185, 0))
            draw_text(frame, "Frame the full side-on kicking action", pos=(30, 80), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(255, 80, 80))
            self.state_tracker["prev_state"] = None
            self.state_tracker["curr_state"] = None

        return frame, play_sound
