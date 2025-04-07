## CRTBlaster

This project runs on a Raspberry Pi. It serves a webpage which lets users upload videos and then queue them 
for playing on a TV.

In principle, there are a few products similar to this on the market (Android TV boxes, etc), but they 
are more focused on streaming media for consumption. CRTBlaster is meant for easily looping queues of video
for decor and art installations.

A web interface is exposed on port 80 that lets anyone on the local wi-fi network connect to upload videos
and select which ones are playing.

## Design
The 

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
