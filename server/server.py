from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import time
import base64
import os
import subprocess
import socket

app = Flask(__name__)

NEW_VIDEO_DIR="../data/new_videos"
PROCESSED_VIDEO_DIR="../data/processed_videos"
THUMBNAIL_DIR="./static/thumbs"
DEFAULT_THUMBNAIL="./static/default_thumbnail.png"

# This is the upload page.
# The user submits uploaded video via this page.
# TODO: add progress bar for user.
@app.route('/')
@app.route('/index')
@app.route('/upload')
def index():
    return render_template('./upload.html')

# This endpoint accepts video uploads from the user.
# TODO: just put the conversion in here instead of in a seperate script
@app.route('/upload/video', methods=['POST'])
def upload_file():
    print(request)
    print(f"video name is {request.form['videoname']}")
    print(request.files['video'])
    request.files['video'].save(f"{NEW_VIDEO_DIR}/{request.form['videoname']}.mp4")
    return ""

# This page lets the user select which videos to play in a loop.
@app.route('/play')
def play():
    return render_template('./play.html')

# Utility function that sorts an array of files by most recent
def sort_files_by_recent(filepaths):
    filepaths.sort(key=lambda x: os.path.getmtime(x))
    filepaths.reverse()
    return filepaths

# This route gives the app a way to fetch a list of all videos
# An array of dicts is sent which tells the client which videos are available.
#     "name": string
#     The name of the video. Unique user-assigned identifier that identifies the video in the system.
#
#     "thumbnail": png
#     180x120 image representing the video
#
#     "processing": bool
#     If this is true, then the thumbnail is invalid. The video is still processing.
@app.route('/upload/videoinfo')
def videoinfo():
    # Get the names of all fully processed videos.
    pending_video_names = os.listdir(NEW_VIDEO_DIR)
    processed_video_names = [name for name in os.listdir(PROCESSED_VIDEO_DIR) if name not in pending_video_names]
    
    # Sort them by most recently modified
    processed_videos_filepaths = sort_files_by_recent([f"{PROCESSED_VIDEO_DIR}/{f}" for f in processed_video_names])
    pending_videos_filepaths = sort_files_by_recent([f"{NEW_VIDEO_DIR}/{f}" for f in pending_video_names])

    # For each video, add it and its thumbnail to the list of videos available to stream.
    videos = []
    processed_video_names = []
    tstart = time.time()
    for videofile in processed_videos_filepaths:
        # Get the video's name. The video's unique user-assigned name is its filename.
        videoname = os.path.splitext(os.path.basename(videofile))[0]
        processed_video_names.append(videoname)
        
        # Retrieve and encode the thumbnail
        thumbname = f"{THUMBNAIL_DIR}/{videoname}.png"
        print(f"videoinfo: {thumbname}")
        thumbnail_url = f"static/thumbs/{videoname}.png"

        videos.append({"name": videoname, "thumbnail_url": thumbnail_url, "processing": False})
    
    # Get all videos not yet in the processed videos folder
    for videofile in pending_videos_filepaths:
        videoname = os.path.splitext(os.path.basename(videofile))[0]
        if (videoname not in processed_video_names):
            thumbname = DEFAULT_THUMBNAIL
            print(f"videoinfo: {thumbname}")

            thumbnail_url = f"static/default_thumbnail.png"
            videos.append({"name": f"{videoname} (processing)", "thumbnail_url": thumbnail_url, "processing": True})
    
    # Send video data
    return jsonify(videos)

@app.route('/playlist/playvideo', methods=['POST'])
def play_video():
    d = request.get_json()
    print("play_video: " + d["name"])
    videoname = d["name"].replace("../", "")

    try:
        output_file = f"{PROCESSED_VIDEO_DIR}/{videoname}.mp4"
        time.sleep(0.1)
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

    return ""


# This endpoint deletes videos
@app.route('/upload/deletevideo', methods=['POST'])
def delete_video():
    d = request.get_json()
    print("delete_video: " + d["name"])
    videoname = d["name"].replace("../", "")
    
    # TODO: double check that video exists and that its in the dirs
    subprocess.run(["rm", f"{THUMBNAIL_DIR}/{videoname}.png"])
    subprocess.run(["rm", f"{PROCESSED_VIDEO_DIR}/{videoname}.mp4"])
    return ""

# Listens for changes in the uploaded videos and playlist.
# Very jenky.
def video_upload_event_stream():
    prev_processed_vids = os.listdir(PROCESSED_VIDEO_DIR)
    prev_new_vids = os.listdir(NEW_VIDEO_DIR)
    while True:
        time.sleep(0.1)
        processed_vids = os.listdir(PROCESSED_VIDEO_DIR)
        new_vids = os.listdir(NEW_VIDEO_DIR)
        if ((processed_vids != prev_processed_vids) or (new_vids != prev_new_vids)):
            yield "data: update\n\n"
        prev_processed_vids = processed_vids
        prev_new_vids = new_vids

# This SSE stream sends a notice whenever the video library or playlist has been updated
@app.route('/upload/videouploadevents')
def videouploadevents():
    return Response(video_upload_event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True, host="0.0.0.0")
