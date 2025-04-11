#!/bin/python3

# Files uploaded may not be in h264.
# This script monitors the directory of newly uploaded videos.
# If a new file that doesn't end in .temp is created, then ffmpeg is used to convert it
# to a file using h264 encoding.

import os
import subprocess
import socket
import sys
import time

input_dir = "./data/new_videos"
output_dir = "./data/processed_videos"
backup_dir = "./data/prev_videos"
thumbnail_dir = "./server/static/thumbs"

supported_extensions = ["mp4", "avi", "mkv"]

target_resolution = (720, 480)

def get_encoding(videofile):
    """ returns the encoding of a video file as a string """
    result = subprocess.run(["ffprobe",
                    "-v", "error",
                    "-select_streams", "v:0",
                    "-show_entries", "stream=codec_name",
                    "-of", "default=nokey=1:noprint_wrappers=1",
                    videofile], capture_output=True, text=True)
    return str(result.stdout)

def get_dims(videofile):
    """ Returns a tuple representing the width x height of
    """
    result = subprocess.run(["ffprobe",
                             "-v", "error",
                             "-select_streams", "v",
                             "-show_entries", "stream=width,height",
                             "-of", "csv=p=0:s=x",
                             videofile], capture_output=True, text=True)
    s = result.stdout
    return (int(s.split('x')[0]), int(s.split('x')[1]))

def daemon():
    # Check to make sure that we're in the project root. If not, abort
    if (os.path.basename(os.getcwd()) != "crtblaster"):
        print(f"Convert daemon should be run from project root. Exiting.")
        sys.exit(-1)

    # Check to see if the correct data directories exist. If not, make them.
    required_dirs = ["./data", input_dir, output_dir, backup_dir, thumbnail_dir]
    for d in required_dirs:
        os.makedirs(d, exist_ok=True)

    # Poll for new videos
    print(f"Waiting for new video files at {input_dir} ...")
    while True:
        time.sleep(0.05)

        # Check to see if there are any new videos to process
        candidate_files = [f for f in os.listdir(input_dir) if f.split(".")[-1] in supported_extensions]
        for f in candidate_files:
            full_input_filename = f"{input_dir}/{f}"
            input_encoding = get_encoding(full_input_filename)
            print(f"input file {f} has encoding {str(input_encoding)}")

            try:
                resolution = get_dims(full_input_filename)
                print(f"input video dimensions are {resolution}")


                #-vf

                print(f"transcoding {f} to h264.")
                proc = subprocess.run(["ffmpeg", "-i", f"{full_input_filename}", "-y",
                                       "-c:v", "libx264", "-crf", "10",
                                       "-threads", "2",
                                       "-vf", "scale=720:480:force_original_aspect_ratio=decrease,pad=720:480:(ow-iw)/2:(oh-ih)/2,setsar=1",
                                       "-preset", "superfast", "-c:a", "copy",
                                       f"{output_dir}/{f}"], check=True)
                print("the commandline is {}".format(proc.args))

                # Make a thumbnail for the video and put it in the thumbnail dir
                fname = os.path.splitext(os.path.basename(f))[0]
                subprocess.run(["ffmpeg",  "-y",
                                "-i", f"{output_dir}/{f}",
                                "-ss", "00:00:01.000",
                                "-vframes", "1",
                                f"{thumbnail_dir}/{fname}.png"])

            except Exception as e:
                print(e)

            # Move the file to the backup dir now that it's processed
            subprocess.run(["rm", f"{input_dir}/{f}"])

if __name__ == "__main__":
    daemon()
