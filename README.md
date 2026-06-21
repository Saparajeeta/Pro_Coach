# 🦾 The Pro Coach - AI Vision-Based Solo Training Assistant

**The Pro Coach** is a high-performance biomechanical assessment platform designed for unconstrained training environments. Leveraging MediaPipe BlazePose landmark extraction pipelines alongside continuous angular heuristic analysis, this application eliminates the traditional supervision gap in home fitness and athletics by providing clinical-grade real-time posture valuation.

## 🌟 Features

- **Real-Time Posture Analysis:** Tracks and evaluates form during various exercises using a webcam or uploaded videos.
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
4. Choose between **Live Stream** (via webcam) or **Upload Video**.
5. Start exercising and receive real-time biomechanical feedback!

## 📁 Project Structure

- `Homepage.py`: Main entry point of the app containing the dashboard and login state.
- `pages/`: Additional Streamlit pages for different exercises and features.
- `process_frame_*.py`: Logic and kinematics for processing specific exercises (curling, lunges, pushups, squats, etc.).
- `threshold_*.py`: Angle thresholds and heuristic definitions for each exercise.
- `audio_feedback.py`: Text-to-speech integration.
- `utils.py`: Helper functions for drawing landmarks and analyzing angles.
- `requirements.txt`: Python package dependencies.

## 📄 License

This project is licensed under the MIT License.
