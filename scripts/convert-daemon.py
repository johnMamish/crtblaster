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

def get_encoding(videofile):
    """ returns the encoding of a video file as a string """
    result = subprocess.run(["ffprobe", 
                    "-v", "error", 
                    "-select_streams", "v:0",
                    "-show_entries", "stream=codec_name", 
                    "-of", "default=nokey=1:noprint_wrappers=1",
                    videofile], capture_output=True, text=True)
    return str(result.stdout)

while True:
    time.sleep(0.1)

    # Check to see if there are any new videos to process
    candidate_files = [f for f in os.listdir(input_dir) if f.split(".")[-1] in supported_extensions]
    for f in candidate_files:
        full_input_filename = f"{input_dir}/{f}"
        input_encoding = get_encoding(full_input_filename)
        print(f"input file {f} has encoding {str(input_encoding)}")
        if (False):
            print(f"Input video {f} is already h264. No transcoding will occur.")
            subprocess.run(["cp", f"{input_dir}/{f}", f"{output_dir}/{f}"])
        else:
            try:
                print(f"transcoding {f} to h264.")
                proc = subprocess.run(["ffmpeg", "-i", f"{full_input_filename}", "-y", 
                                "-c:v", "libx264", "-crf", "10", 
                                "-threads", "2",
                                "-filter:v", "scale=320:-1",
                                "-preset", "superfast", "-c:a", "copy", 
                                f"{output_dir}/{f}"], check=True)
                print("the commandline is {}".format(proc.args))
            except Exception as e:
                print(e)

        # Make a thumbnail for the video and put it in the thumbnail dir
        fname = os.path.splitext(os.path.basename(f))[0]
        subprocess.run(["ffmpeg",  "-y",
                        "-i", f"{output_dir}/{f}", 
                        "-ss", "00:00:01.000", 
                        "-vframes", "1", 
                        f"{thumbnail_dir}/{fname}.png"])

        # Move the file to the backup dir now that it's processed
        subprocess.run(["mv", f"{input_dir}/{f}", f"{backup_dir}/{f}"])
        
        # Optional: play the file via the VLC interface
        continue
        try:
            output_file = f"{backup_dir}/{f}"
            time.sleep(1)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(("localhost", 14484))
                time.sleep(0.1)
                sock.sendall(f"clear\r\n".encode("utf-8"))
                time.sleep(0.1)
                sock.sendall(f"add {os.path.abspath(output_file)}\r\n".encode("utf-8"))
                time.sleep(0.1)
                sock.sendall(f"play\r\n".encode("utf-8"))
                time.sleep(0.1)
                sock.sendall(f"repeat on\r\n".encode("utf-8"))
        except Exception as e:
            print(e)

