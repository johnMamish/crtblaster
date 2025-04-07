For the videoserver to run, the following processes need to be started

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
