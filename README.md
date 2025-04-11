## CRTBlaster

This project runs on a Raspberry Pi. It serves a webpage which lets users upload videos and then queue them
for playing on a TV.

In principle, there are a few products similar to this on the market (Android TV boxes, etc), but they
are more focused on streaming media for consumption. CRTBlaster is meant for easily looping queues of video
for decor, art installations, and performances.

A web interface is exposed on port 80 that lets anyone on the local wi-fi network connect to upload videos
and select which ones are playing.

## Setup
### Operating system
You *must* use an older version of Raspberry pi OS. The November 2024 version doesn't correctly support CRT output.

I'm using `2022-09-22-raspios-buster-armhf.img`.

### CRT configure
use `sudo raspi-config` to enable CRT output

### Directories
There should be a user called `john` and the crtblaster repo should be in its home dir.

### Services
Copy files from `crtblaster/services/` to `/etc/systemd/system/` and then run

```
sudo systemctl enable crtblaster-server.service
sudo systemctl enable headlessvlc.service
sudo systemctl enable crtblaster-convert-daemon.service
```

### VLC
You'll probably need to click through some VLC menus.

## Design
### Web interface
#### Data uploading
At /index, there's a data upload page which lets users upload one video at a time.

Uploaded videos will automatically be re-encoded on the server for optimal playback.
At a minimum, this means:
  - Re-encoding in h264
  - Adjustment of video size to 720x480.

The user can also optionally specify
  - Conversion from color to black / white
  - During resolution change whether video should be stretched or whether vbars / hbars should be added

#### Playlist queueing
At /play, there's a page that lets users browse all uploaded videos and select which ones are playing.
It also controls looping.

We do have an option to allow users to toggle to the 'next' video in the playlist before the current
one is done playing.

### Data storage
Videos are stored in the 'data' folder.

When videos are uploaded, they may not be in the right format. CRTBlaster will process any uploaded video
to make sure that its aspect ratio and encoding are correct.

Newly uploaded videos go in `data/new_videos` while they undergo processing.

Once a video has been processed, it goes in `data/processed_videos`.
Videos that are successfully processed are deleted from `new_videos` and optionally backed up in `data/prev_videos`.
If a video fails processing for whatever reason, it's put in `failed_videos`.

## Starting CRTBlaster
For CRTBlaster run, the following processes need to be started

##### Start the flask app that serves the webpage and accepts uploads
```
cd ./server
flask --app server --debug run --host=0.0.0.0
```

###### Start a daemon that monitors for new uploads and converts them
This daemon also tells vlc to play the video
Run from root project dir
```
./scripts/convert-daemon.py
```

##### Start VLC
```
./scripts/vlc-startup.sh
```
