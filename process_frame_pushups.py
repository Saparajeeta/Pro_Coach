import time
import cv2
import numpy as np
from utils import find_angle, get_landmark_features, draw_text, draw_dotted_line, log_mistake
from audio_feedback import play_audio

class ProcessFramePushup:
    def __init__(self, thresholds, flip_frame=False):
        self.flip_frame = flip_frame
        self.thresholds = thresholds
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.linetype = cv2.LINE_AA

        self.COLORS = {
            'blue'       : (0, 127, 255),
            'red'        : (255, 50, 50),
            'green'      : (0, 255, 127),
            'light_green': (100, 233, 127),
            'yellow'     : (255, 255, 0),
            'magenta'    : (255, 0, 255),
            'white'      : (255,255,255),
            'cyan'       : (0, 255, 255),
            'light_blue' : (102, 204, 255),
            'rose'       : (255,102,204),
            'aqua'       : (192, 220, 205)
        }

        self.dict_features = {}
        self.left_features = {
            'shoulder': 11, 'elbow': 13, 'wrist': 15, 'hip': 23, 'knee': 25, 'ankle': 27, 'foot': 31
        }
        self.right_features = {
            'shoulder': 12, 'elbow': 14, 'wrist': 16, 'hip': 24, 'knee': 26, 'ankle': 28, 'foot': 32
        }
        self.dict_features['left'] = self.left_features
        self.dict_features['right'] = self.right_features
        self.dict_features['nose'] = 0

        self.state_tracker = {
            'state_seq': [],
            'start_inactive_time': time.perf_counter(),
            'INACTIVE_TIME': 0.0,
            'DISPLAY_TEXT' : np.full((2,), False),
            'COUNT_FRAMES' : np.zeros((2,), dtype=np.int64),
            'INCORRECT_POSTURE': False,
            'prev_state': None,
            'curr_state': None,
            'PUSHUP_COUNT': 0,
            'IMPROPER_PUSHUP': 0
        }
        
        self.FEEDBACK_ID_MAP = {
            0: ('KEEP BACK STRAIGHT', 215, (0, 153, 255)),
            1: ('GO LOWER', 170, (255, 80, 80))
        }

    def _get_state(self, elbow_angle):
        state = None
        if self.thresholds['ELBOW_ANGLE']['NORMAL'][0] >= elbow_angle >= self.thresholds['ELBOW_ANGLE']['NORMAL'][1]:
            state = 1
        elif self.thresholds['ELBOW_ANGLE']['TRANS'][0] >= elbow_angle >= self.thresholds['ELBOW_ANGLE']['TRANS'][1]:
            state = 2
        elif self.thresholds['ELBOW_ANGLE']['PASS'][0] >= elbow_angle >= self.thresholds['ELBOW_ANGLE']['PASS'][1]:
            state = 3
        return f's{state}' if state else None

    def _update_state_sequence(self, state):
        if state == 's2':
            if (('s3' not in self.state_tracker['state_seq']) and (self.state_tracker['state_seq'].count('s2'))==0) or \
               (('s3' in self.state_tracker['state_seq']) and (self.state_tracker['state_seq'].count('s2')==1)):
                self.state_tracker['state_seq'].append(state)
        elif state == 's3':
            if (state not in self.state_tracker['state_seq']) and 's2' in self.state_tracker['state_seq']: 
                self.state_tracker['state_seq'].append(state)

    def _show_feedback(self, frame, c_frame, dict_maps):
        for idx in np.where(c_frame)[0]:
            draw_text(
                frame, dict_maps[idx][0], pos=(30, dict_maps[idx][1]),
                text_color=(255, 255, 230), font_scale=0.6, text_color_bg=dict_maps[idx][2]
            )
        return frame

    def process(self, frame: np.array, pose):
        play_sound = None
        frame_height, frame_width, _ = frame.shape
        keypoints = pose.process(frame)

        if keypoints.pose_landmarks:
            ps_lm = keypoints.pose_landmarks

            left_shldr_coord, left_elbow_coord, left_wrist_coord, left_hip_coord, left_knee_coord, left_ankle_coord, left_foot_coord = \
                get_landmark_features(ps_lm.landmark, self.dict_features, 'left', frame_width, frame_height)
            right_shldr_coord, right_elbow_coord, right_wrist_coord, right_hip_coord, right_knee_coord, right_ankle_coord, right_foot_coord = \
                get_landmark_features(ps_lm.landmark, self.dict_features, 'right', frame_width, frame_height)

            # Determine side closer to camera
            dist_l = abs(left_shldr_coord[0] - left_wrist_coord[0]) + abs(left_shldr_coord[1] - left_foot_coord[1])
            dist_r = abs(right_shldr_coord[0] - right_wrist_coord[0]) + abs(right_shldr_coord[1] - right_foot_coord[1])

            if dist_l > dist_r:
                shldr_coord, elbow_coord, wrist_coord, hip_coord, knee_coord = left_shldr_coord, left_elbow_coord, left_wrist_coord, left_hip_coord, left_knee_coord
            else:
                shldr_coord, elbow_coord, wrist_coord, hip_coord, knee_coord = right_shldr_coord, right_elbow_coord, right_wrist_coord, right_hip_coord, right_knee_coord

            elbow_angle = find_angle(shldr_coord, wrist_coord, ref_pt=elbow_coord)
            hip_angle = find_angle(shldr_coord, knee_coord, ref_pt=hip_coord)

            cv2.line(frame, shldr_coord, elbow_coord, self.COLORS['aqua'], 4, lineType=self.linetype)
            cv2.line(frame, wrist_coord, elbow_coord, self.COLORS['aqua'], 4, lineType=self.linetype)
            cv2.line(frame, shldr_coord, hip_coord, self.COLORS['aqua'], 4, lineType=self.linetype)
            cv2.line(frame, hip_coord, knee_coord, self.COLORS['aqua'], 4, lineType=self.linetype)

            cv2.circle(frame, shldr_coord, 7, self.COLORS['rose'], -1, lineType=self.linetype)
            cv2.circle(frame, elbow_coord, 7, self.COLORS['rose'], -1, lineType=self.linetype)
            cv2.circle(frame, wrist_coord, 7, self.COLORS['rose'], -1, lineType=self.linetype)
            cv2.circle(frame, hip_coord, 7, self.COLORS['rose'], -1, lineType=self.linetype)
            cv2.circle(frame, knee_coord, 7, self.COLORS['rose'], -1, lineType=self.linetype)

            current_state = self._get_state(int(elbow_angle))
            self.state_tracker['curr_state'] = current_state
            self._update_state_sequence(current_state)

            if current_state == 's1':
                if len(self.state_tracker['state_seq']) == 3 and not self.state_tracker['INCORRECT_POSTURE']:
                    self.state_tracker['PUSHUP_COUNT'] += 1
                    play_sound = str(self.state_tracker['PUSHUP_COUNT'])
                    play_audio(f"Good. {self.state_tracker['PUSHUP_COUNT']}")
                elif 's2' in self.state_tracker['state_seq'] and len(self.state_tracker['state_seq']) == 1:
                    self.state_tracker['IMPROPER_PUSHUP'] += 1
                    play_sound = 'incorrect'
                    play_audio("Go lower")
                elif self.state_tracker['INCORRECT_POSTURE']:
                    self.state_tracker['IMPROPER_PUSHUP'] += 1
                    play_sound = 'incorrect'
                self.state_tracker['state_seq'] = []
                self.state_tracker['INCORRECT_POSTURE'] = False
            else:
                if hip_angle < self.thresholds['HIP_ANGLE_THRESH']:
                    self.state_tracker['DISPLAY_TEXT'][0] = True
                    self.state_tracker['INCORRECT_POSTURE'] = True
                    if self.state_tracker['COUNT_FRAMES'][0] == 0:
                        play_audio("Keep your back straight")
                        log_mistake("Sagging Back in Pushups")

            display_inactivity = False
            if self.state_tracker['curr_state'] == self.state_tracker['prev_state']:
                end_time = time.perf_counter()
                self.state_tracker['INACTIVE_TIME'] += end_time - self.state_tracker['start_inactive_time']
                self.state_tracker['start_inactive_time'] = end_time
                if self.state_tracker['INACTIVE_TIME'] >= self.thresholds['INACTIVE_THRESH']:
                    self.state_tracker['PUSHUP_COUNT'] = 0
                    self.state_tracker['IMPROPER_PUSHUP'] = 0
                    display_inactivity = True
            else:
                self.state_tracker['start_inactive_time'] = time.perf_counter()
                self.state_tracker['INACTIVE_TIME'] = 0.0

            if self.flip_frame:
                frame = cv2.flip(frame, 1)

            self.state_tracker['COUNT_FRAMES'][self.state_tracker['DISPLAY_TEXT']] += 1
            frame = self._show_feedback(frame, self.state_tracker['COUNT_FRAMES'], self.FEEDBACK_ID_MAP)

            cv2.putText(frame, str(int(elbow_angle)), (elbow_coord[0]+15, elbow_coord[1]+10), self.font, 0.6, self.COLORS['light_green'], 2, lineType=self.linetype)
            cv2.putText(frame, str(int(hip_angle)), (hip_coord[0]+15, hip_coord[1]+10), self.font, 0.6, self.COLORS['light_green'], 2, lineType=self.linetype)

            draw_text(frame, "CORRECT: " + str(self.state_tracker['PUSHUP_COUNT']), pos=(int(frame_width*0.68), 30), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(18, 185, 0))  
            draw_text(frame, "INCORRECT: " + str(self.state_tracker['IMPROPER_PUSHUP']), pos=(int(frame_width*0.68), 80), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(221, 0, 0))  
            
            self.state_tracker['DISPLAY_TEXT'][self.state_tracker['COUNT_FRAMES'] > self.thresholds['CNT_FRAME_THRESH']] = False
            self.state_tracker['COUNT_FRAMES'][self.state_tracker['COUNT_FRAMES'] > self.thresholds['CNT_FRAME_THRESH']] = 0    
            self.state_tracker['prev_state'] = current_state

        else:
            if self.flip_frame:
                frame = cv2.flip(frame, 1)
            end_time = time.perf_counter()
            self.state_tracker['INACTIVE_TIME'] += end_time - self.state_tracker['start_inactive_time']
            if self.state_tracker['INACTIVE_TIME'] >= self.thresholds['INACTIVE_THRESH']:
                self.state_tracker['PUSHUP_COUNT'] = 0
                self.state_tracker['IMPROPER_PUSHUP'] = 0
            self.state_tracker['start_inactive_time'] = end_time

            draw_text(frame, "CORRECT: " + str(self.state_tracker['PUSHUP_COUNT']), pos=(int(frame_width*0.68), 30), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(18, 185, 0))  
            draw_text(frame, "INCORRECT: " + str(self.state_tracker['IMPROPER_PUSHUP']), pos=(int(frame_width*0.68), 80), text_color=(255, 255, 230), font_scale=0.7, text_color_bg=(221, 0, 0))  

            self.state_tracker['prev_state'] =  None
            self.state_tracker['curr_state'] = None
            self.state_tracker['INCORRECT_POSTURE'] = False
            self.state_tracker['DISPLAY_TEXT'] = np.full((2,), False)
            self.state_tracker['COUNT_FRAMES'] = np.zeros((2,), dtype=np.int64)
            
        return frame, play_sound
