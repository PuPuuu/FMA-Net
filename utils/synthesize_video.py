#!/usr/bin/env python3
"""Synthesize a video from a folder of frames."""

import argparse
import glob
import os
import cv2


def synthesize_video(
    frames_dir: str,
    output_path: str = None,
    fps: float = 30.0,
    ext: str = "png",
    codec: str = "mp4v",
):
    """
    Combine frames in a directory into a video.

    Args:
        frames_dir:  Directory containing frame images (sorted by filename).
        output_path: Output video path. Defaults to <frames_dir>.mp4.
        fps:         Frame rate of the output video.
        ext:         Frame file extension to look for (default: png).
        codec:       FourCC codec string (default: mp4v).
    """
    pattern = os.path.join(frames_dir, f"*.{ext.lstrip('.')}")
    frame_paths = sorted(glob.glob(pattern))
    if not frame_paths:
        raise RuntimeError(f"No .{ext} files found in: {frames_dir}")

    # Read first frame to get dimensions
    first = cv2.imread(frame_paths[0])
    if first is None:
        raise RuntimeError(f"Cannot read frame: {frame_paths[0]}")
    h, w = first.shape[:2]

    if output_path is None:
        output_path = frames_dir.rstrip("/\\") + ".mp4"

    fourcc = cv2.VideoWriter_fourcc(*codec)
    writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    if not writer.isOpened():
        raise RuntimeError(f"Cannot open VideoWriter for: {output_path}")

    for path in frame_paths:
        frame = cv2.imread(path)
        if frame is None:
            print(f"  Warning: skipping unreadable frame {path}")
            continue
        writer.write(frame)

    writer.release()
    print(f"Synthesized {len(frame_paths)} frames -> {output_path}  (fps={fps}, size={w}x{h})")


def main():
    parser = argparse.ArgumentParser(description="Synthesize a video from frames.")
    parser.add_argument("frames_dir", help="Directory containing frame images")
    parser.add_argument(
        "--output", default=None,
        help="Output video path (default: <frames_dir>.mp4)"
    )
    parser.add_argument(
        "--fps", type=float, default=30.0,
        help="Output frame rate (default: 30)"
    )
    parser.add_argument(
        "--ext", default="png",
        help="Frame file extension to look for (default: png)"
    )
    parser.add_argument(
        "--codec", default="mp4v",
        help="FourCC codec string (default: mp4v)"
    )
    args = parser.parse_args()
    synthesize_video(
        frames_dir=args.frames_dir,
        output_path=args.output,
        fps=args.fps,
        ext=args.ext,
        codec=args.codec,
    )


if __name__ == "__main__":
    main()
