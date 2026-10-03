import csv
import os
import sys
import time
from statistics import mean, pstdev

import cv2

from process_frame_pushups import ProcessFramePushup
from threshold_pushups import get_thresholds_beginner
from utils import get_mediapipe_pose


def benchmark_video(video_path):
    if not video_path or not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    pose = get_mediapipe_pose()
    process_frame = ProcessFramePushup(get_thresholds_beginner())

    video_read_ms = []
    pose_process_ms = []
    pushup_process_remaining_ms = []
    combined_total_ms = []
    total_latency_ms = []
    frame_rows = []

    frame_index = 0
    while True:
        start = time.perf_counter()
        ok, frame = cap.read()
        if not ok:
            break

        frame_index += 1
        video_read_ms.append((time.perf_counter() - start) * 1000.0)

        if frame_index <= 30:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pose_start = time.perf_counter()
        pose.process(rgb_frame)
        pose_ms = (time.perf_counter() - pose_start) * 1000.0
        pose_process_ms.append(pose_ms)

        combined_start = time.perf_counter()
        process_frame.process(rgb_frame, pose)
        combined_ms = (time.perf_counter() - combined_start) * 1000.0
        combined_total_ms.append(combined_ms)

        remaining_ms = max(0.0, combined_ms - pose_ms)
        pushup_process_remaining_ms.append(remaining_ms)

        total_ms = video_read_ms[-1] + pose_ms + remaining_ms
        total_latency_ms.append(total_ms)

        frame_rows.append(
            {
                "frame": frame_index,
                "video_read_ms": video_read_ms[-1],
                "pose_process_ms_approx": pose_ms,
                "process_remainder_ms_approx": remaining_ms,
                "combined_process_total_ms": combined_ms,
                "total_latency_ms": total_ms,
            }
        )

    cap.release()

    if not total_latency_ms:
        raise ValueError(f"No valid frames processed from {video_path}")

    csv_path = "benchmark_results.csv"
    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "frame",
                "video_read_ms",
                "pose_process_ms_approx",
                "process_remainder_ms_approx",
                "combined_process_total_ms",
                "total_latency_ms",
            ],
        )
        writer.writeheader()
        writer.writerows(frame_rows)

    print("Stage timing summary (approximate split because ProcessFramePushup.process contains the pose call internally):")
    print(f"Video read mean: {mean(video_read_ms[30:]):.2f} ms, std: {pstdev(video_read_ms[30:]):.2f} ms")
    print(f"Pose.process mean: {mean(pose_process_ms):.2f} ms, std: {pstdev(pose_process_ms):.2f} ms")
    print(f"Pushup remainder mean: {mean(pushup_process_remaining_ms):.2f} ms, std: {pstdev(pushup_process_remaining_ms):.2f} ms")
    print(f"Total mean latency: {mean(total_latency_ms):.2f} ms")
    print(f"FPS = 1000 / total mean = {1000.0 / mean(total_latency_ms):.2f}")
    print(f"Per-frame timings written to {csv_path}")

    return {
        "video_read_ms": video_read_ms[30:],
        "pose_process_ms": pose_process_ms,
        "pushup_process_remaining_ms": pushup_process_remaining_ms,
        "total_latency_ms": total_latency_ms,
        "fps": 1000.0 / mean(total_latency_ms),
    }


if __name__ == "__main__":
    video_path = sys.argv[1] if len(sys.argv) > 1 else "output_sample.mp4"
    benchmark_video(video_path)
