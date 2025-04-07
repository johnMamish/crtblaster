#!/bin/bash

# This file contains a command that starts vlc in full screen and with an interface that lets 
# you control it over port 14484

# https://n0tablog.wordpress.com/2009/02/09/
# controlling-vlc-via-rc-remote-control-interface-using-a-unix-domain-socket-and-no-programming/

DISPLAY=:0 vlc --extraintf=rc --rc-host=localhost:14484 --fullscreen
