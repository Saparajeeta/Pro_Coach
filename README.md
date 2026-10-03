# 🦾 The Pro Coach - AI Vision-Based Solo Training Assistant

**The Pro Coach** is a high-performance biomechanical assessment platform designed for unconstrained training environments. Leveraging MediaPipe BlazePose landmark extraction pipelines alongside continuous angular heuristic analysis, this application eliminates the traditional supervision gap in home fitness and athletics by providing clinical-grade real-time posture valuation.

## 🌟 Features

- **Real-Time Posture Analysis:** Tracks and evaluates form during various exercises using a webcam.
- **Multiple Supported Exercises:** 
  - Bicep Curls
  - Squats
  - Lunges
  - Pushups
  - Tricep Kickbacks
- **Gamification Dashboard:** Level tracking, total XP, and active streaks to keep you motivated.
- **Audio Feedback:** Real-time verbal corrections and guidance for your form.
- **Secure Authentication:** User login system to track individual progress and history.

## 🛠️ Technology Stack

- **Python:** Core programming language.
- **Streamlit:** Web framework for the interactive user interface.
- **MediaPipe:** High-fidelity ML pipeline for pose estimation and body tracking.
- **OpenCV:** Computer vision library for frame processing.
- **Plotly:** Interactive data visualizations.
- **Pyttsx3:** Text-to-speech conversion for audio feedback.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Webcam for live stream analysis

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Execute the following command in the terminal to launch the Streamlit app:
```bash
streamlit run Homepage.py
```

### Usage

1. Open the app in your browser (usually `http://localhost:8501`).
2. Log in using your credentials.
3. Select an active workspace module from the sidebar (e.g., Pushups, Squats).
4. Start exercising and receive real-time biomechanical feedback!

## 📁 Project Structure

- `Homepage.py`: Main entry point of the app containing the dashboard and login state.
- `pages/`: Additional Streamlit pages for different exercises and features.
- `process_frame_*.py`: Logic and kinematics for processing specific exercises (curling, lunges, pushups, squats, etc.).
- `threshold_*.py`: Angle thresholds and heuristic definitions for each exercise.
- `audio_feedback.py`: Text-to-speech integration.
- `utils.py`: Helper functions for drawing landmarks and analyzing angles.
- `requirements.txt`: Python package dependencies.

## Data and Model Provenance
- Approach: this project uses a pretrained pose-estimation model (transfer of an existing model) instead of training a new one. Pose landmarks come from the pretrained MediaPipe Pose (BlazePose) model that is bundled inside the mediapipe package (version pinned in requirements.txt). BlazePose is designed for real-time, CPU-only inference.
- Training data: the BlazePose weights were trained by their authors (Google) on their own data. That data is not part of this repository and was not used or modified here. No model was trained or fine-tuned in this project, and this repository contains no training dataset.
- Our contribution: converting landmarks to joint and segment-to-vertical angles, exercise-specific finite state machines for repetition counting, rule-based form checks, voice and visual feedback, and the Streamlit web application.
- Rule-based logic: thresholds are hand-set and defined in thresholds.py, threshold_pushups.py, threshold_curl.py, threshold_kickback.py and threshold_lunges.py, and in the page scripts of the additional exercises. They are not learned from data.
- OpenPose is not used.
- Evaluation data: our own recorded exercise videos and manual labels are not part of this repository. See evaluation/README.md for the protocol and how accuracy is computed from evaluation/trials.csv.
- output_sample.mp4 is a bicep-curl demonstration video used on the Demo page.
- References: C. Lugaresi et al., "MediaPipe: A framework for building perception pipelines," arXiv:1906.08172, 2019. V. Bazarevsky et al., "BlazePose: On-device real-time body pose tracking," arXiv:2006.10204, 2020.

## 📄 Copyright & License

© 2026 Aparajeeta. All Rights Reserved. 
This is a proprietary final year academic project. Unauthorized copying, modification, distribution, or use of this repository is strictly prohibited without explicit permission.
