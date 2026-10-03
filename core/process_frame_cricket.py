import time

import cv2
import numpy as np

from utils import draw_text, find_angle, get_landmark_features


class ProcessFrameCricket:
    def __init__(self, thresholds=None, flip_frame=False):
        self.thresholds = thresholds or {
            "FRONT_KNEE_ANGLE": (110, 170),
            "TRUNK_TILT": 22,
            "ELBOW_EXTENSION": 145,
            "BOWLING_LOAD": 80,
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
            "CRICKET_COUNT": 0,
            "IMPROPER_BOWLING": 0,
            "start_inactive_time": time.perf_counter(),
            "INACTIVE_TIME": 0.0,
        }
        self.FEEDBACK_ID_MAP = {
            0: ("FRONT KNEE TOO STRAIGHT", 175, (255, 80, 80)),
            1: ("KEEP TRUNK TALL", 140, (0, 153, 255)),
            2: ("SMOOTHER ELBOW EXTENSION", 105, (255, 80, 80)),
            3: ("LOAD THE BACK LEG", 70, (0, 153, 255)),
        }

    def _choose_side(self, left_shoulder, right_shoulder, left_hip, right_hip):
        left_center = np.mean([left_shoulder, left_hip], axis=0)
        right_center = np.mean([right_shoulder, right_hip], axis=0)
        return "left" if left_center[0] < right_center[0] else "right"

    def _get_state(self, elbow_angle, front_knee_angle, trunk_angle):
        if elbow_angle < 120 and front_knee_angle > 110 and trunk_angle < 25:
            return "s1"
        if elbow_angle >= 150 and front_knee_angle > 100 and trunk_angle < 28:
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
            left_shoulder = get_landmark_features(lm, self.dict_features, "left", frame_width, frame_height)[0]
            right_shoulder = get_landmark_features(lm, self.dict_features, "right", frame_width, frame_height)[0]
            left_hip = get_landmark_features(lm, self.dict_features, "left", frame_width, frame_height)[3]
            right_hip = get_landmark_features(lm, self.dict_features, "right", frame_width, frame_height)[3]
            side = self._choose_side(left_shoulder, right_shoulder, left_hip, right_hip)

            if side == "left":
                shoulder, elbow, wrist, hip, knee, ankle, foot = get_landmark_features(lm, self.dict_features, "left", frame_width, frame_height)
                support_shoulder, support_elbow, support_wrist, support_hip, support_knee, support_ankle, support_foot = get_landmark_features(lm, self.dict_features, "right", frame_width, frame_height)
            else:
                support_shoulder, support_elbow, support_wrist, support_hip, support_knee, support_ankle, support_foot = get_landmark_features(lm, self.dict_features, "left", frame_width, frame_height)
                shoulder, elbow, wrist, hip, knee, ankle, foot = get_landmark_features(lm, self.dict_features, "right", frame_width, frame_height)

            elbow_angle = find_angle(shoulder, elbow, ref_pt=wrist)
            trunk_angle = find_angle(np.array([shoulder[0], shoulder[1] - 40]), shoulder, ref_pt=hip)
            front_knee_angle = find_angle(hip, knee, ref_pt=ankle)
            support_knee_angle = find_angle(support_hip, support_knee, ref_pt=support_ankle)
            plant_spacing = abs(foot[0] - support_foot[0])

            cv2.line(frame, shoulder, elbow, self.COLORS["aqua"], 4, lineType=self.linetype)
            cv2.line(frame, elbow, wrist, self.COLORS["aqua"], 4, lineType=self.linetype)
            cv2.line(frame, hip, knee, self.COLORS["aqua"], 4, lineType=self.linetype)
            cv2.line(frame, knee, ankle, self.COLORS["aqua"], 4, lineType=self.linetype)
            cv2.circle(frame, shoulder, 7, self.COLORS["rose"], -1)
            cv2.circle(frame, elbow, 7, self.COLORS["rose"], -1)
            cv2.circle(frame, wrist, 7, self.COLORS["rose"], -1)
            cv2.circle(frame, hip, 7, self.COLORS["rose"], -1)
            cv2.circle(frame, knee, 7, self.COLORS["rose"], -1)

            state = self._get_state(int(elbow_angle), int(front_knee_angle), int(trunk_angle))
            self.state_tracker["curr_state"] = state
            self._update_state_sequence(state)

            if state == "s2" and self.state_tracker["state_seq"] == ["s1", "s2"]:
                self.state_tracker["CRICKET_COUNT"] += 1
                play_sound = str(self.state_tracker["CRICKET_COUNT"])
                self.state_tracker["state_seq"] = []
                self.state_tracker["INCORRECT_POSTURE"] = False

            if front_knee_angle < self.thresholds["FRONT_KNEE_ANGLE"][0]:
                self.state_tracker["DISPLAY_TEXT"][0] = True
                self.state_tracker["INCORRECT_POSTURE"] = True
            if trunk_angle > self.thresholds["TRUNK_TILT"]:
                self.state_tracker["DISPLAY_TEXT"][1] = True
                self.state_tracker["INCORRECT_POSTURE"] = True
            if elbow_angle < self.thresholds["ELBOW_EXTENSION"] and support_knee_angle > 120:
                self.state_tracker["DISPLAY_TEXT"][2] = True
                self.state_tracker["INCORRECT_POSTURE"] = True
            if plant_spacing < 70:
                self.state_tracker["DISPLAY_TEXT"][3] = True
                self.state_tracker["INCORRECT_POSTURE"] = True

            if self.state_tracker["curr_state"] == self.state_tracker["prev_state"]:
                end_time = time.perf_counter()
                self.state_tracker["INACTIVE_TIME"] += end_time - self.state_tracker["start_inactive_time"]
                self.state_tracker["start_inactive_time"] = end_time
                if self.state_tracker["INACTIVE_TIME"] >= 12.0:
                    self.state_tracker["CRICKET_COUNT"] = 0
                    self.state_tracker["IMPROPER_BOWLING"] = 0
            else:
                self.state_tracker["start_inactive_time"] = time.perf_counter()
                self.state_tracker["INACTIVE_TIME"] = 0.0

            if self.flip_frame:
                frame = cv2.flip(frame, 1)

            frame = self._show_feedback(frame, self.state_tracker["DISPLAY_TEXT"], self.FEEDBACK_ID_MAP)
            cv2.putText(frame, f"Rep: {self.state_tracker['CRICKET_COUNT']}", (30, 30), self.font, 0.8, self.COLORS["green"], 2, cv2.LINE_AA)
            draw_text(frame, f"Shoulder line: {int(trunk_angle)}°", pos=(int(frame_width * 0.68), 30), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(18, 185, 0))
            draw_text(frame, f"Plant gap: {int(plant_spacing)} px", pos=(int(frame_width * 0.68), 80), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(0, 120, 180))

            self.state_tracker["DISPLAY_TEXT"] = np.full((4,), False)
            self.state_tracker["prev_state"] = self.state_tracker["curr_state"]
        else:
            if self.flip_frame:
                frame = cv2.flip(frame, 1)
            draw_text(frame, f"Rep: {self.state_tracker['CRICKET_COUNT']}", pos=(30, 30), text_color=(255, 255, 230), font_scale=0.8, text_color_bg=(18, 185, 0))
            draw_text(frame, "Frame the full body side-on", pos=(30, 80), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(255, 80, 80))
            self.state_tracker["prev_state"] = None
            self.state_tracker["curr_state"] = None

        return frame, play_sound
