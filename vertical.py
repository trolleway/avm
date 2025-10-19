#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

# Hard-coded Movies directory under your home
MOVIES_DIR = os.path.join(os.path.expanduser("~"), "Videos")
# Supported video extensions
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"}

def rotate_video(input_path,flag_resize=True):
    root, ext = os.path.splitext(input_path)
    if ext.lower() not in VIDEO_EXTS:
        print(f"Skipping unsupported extension: {input_path}")
        return
    if root.endswith("_rotated"):
        print(f"Already rotated, skipping: {input_path}")
        return
    scalecmd = ''
    if flag_resize:
        scalecmd = ',scale=-1:1920'
    
    output_path = f"{root}_rotated{ext}"
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf", "transpose=1"+scalecmd,
        "-c:a", "copy",
        output_path
    ]

    print(f"Rotating: {os.path.basename(input_path)} → {os.path.basename(output_path)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Error processing {input_path}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Rotate videos in ~/Movies by 90° for TikTok."
    )
    parser.add_argument(
        "-i", "--input", dest="file",
        help="Process only this file (by absolute path)")
    group_resize = parser.add_mutually_exclusive_group()
    group_resize.add_argument("--resize",action="store_true",dest="flag_resize",default=True,help="resize for social netrorks")
    group_resize.add_argument("--no-resize",action="store_false",dest="flag_resize")
    args = parser.parse_args()

    if args.file:
        target = args.file
        flag_resize=args.flag_resize
        # Allow absolute or relative paths
        #if not os.path.isabs(target):
        #    target = os.path.join(MOVIES_DIR, target)
        if os.path.isfile(target):
            rotate_video(target,flag_resize)
        else:
            print(f"File not found: {target}", file=sys.stderr)
            sys.exit(1)
    else:
        # Batch-process all videos in the directory
        flag_scale=True
        for fname in os.listdir(MOVIES_DIR):
            path = os.path.join(MOVIES_DIR, fname)
            if os.path.isfile(path):
                rotate_video(path, flag_resize)

if __name__ == "__main__":
    main()
