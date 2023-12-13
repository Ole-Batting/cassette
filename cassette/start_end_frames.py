import argparse
import glob
import os

import cv2

def start_end_frame(file_path):
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file - {file_path}")
        return

    # Get total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Read the first frame
    ret, first_frame = cap.read()
    if not ret:
        print(f"Error: Could not read the first frame from {file_path}")
        return

    # Read the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
    ret, last_frame = cap.read()
    if not ret:
        print(f"Error: Could not read the last frame from {file_path}")
        return

    # Release the video capture object
    cap.release()

    return first_frame, last_frame


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True)
    parser.add_argument('-t', type=str, default="mp4")
    args = parser.parse_args()

    if os.path.isdir(args.f):
        for file_path in glob.glob(os.path.join(args.f, f"*.{args.t}")):
            first, last = start_end_frame(file_path)
            cv2.imwrite(f"{file_path.replace(f'.{args.t}', '_first.png')}", first)
            cv2.imwrite(f"{file_path.replace(f'.{args.t}', '_last.png')}", last)

