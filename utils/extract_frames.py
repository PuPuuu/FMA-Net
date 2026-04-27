#!/usr/bin/env python3
"""Extract frames from a video file."""

import argparse
import os
import cv2


def extract_frames(video_path: str, every_n: int = 1, fps: float = None, output_dir: str = "data"):
    """
    Extract frames from a video.

    Args:
        video_path: Path to the input video.
        every_n:    Save every N-th frame (default: 1, i.e. all frames).
        fps:        If set, extract at this frame rate instead of every_n.
        output_dir: Root output directory (frames go to output_dir/<video_stem>/).
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Determine step between saved frames
    if fps is not None:
        if fps <= 0 or fps > video_fps:
            raise ValueError(f"fps must be in (0, {video_fps:.2f}]")
        step = max(1, round(video_fps / fps))
    else:
        step = max(1, every_n)

    video_stem = os.path.splitext(os.path.basename(video_path))[0]
    save_dir = os.path.join(output_dir, video_stem)
    os.makedirs(save_dir, exist_ok=True)

    saved = 0
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % step == 0:
            filename = os.path.join(save_dir, f"{frame_idx:06d}.png")
            cv2.imwrite(filename, frame)
            saved += 1
        frame_idx += 1

    cap.release()
    print(f"Extracted {saved}/{total} frames -> {save_dir}  (step={step}, source_fps={video_fps:.2f})")
    return save_dir


def main():
    parser = argparse.ArgumentParser(description="Extract frames from a video.")
    parser.add_argument("video", help="Input video file")
    parser.add_argument(
        "--every-n", type=int, default=1, metavar="N",
        help="Save every N-th frame (default: 1)"
    )
    parser.add_argument(
        "--fps", type=float, default=None,
        help="Target extraction frame rate (overrides --every-n)"
    )
    parser.add_argument(
        "--output-dir", default="data",
        help="Root output directory (default: data)"
    )
    args = parser.parse_args()
    extract_frames(args.video, every_n=args.every_n, fps=args.fps, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
