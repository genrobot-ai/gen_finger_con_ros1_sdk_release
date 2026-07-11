#!/bin/bash

echo "Starting robot system..."
# source ~/robot_ws/devel/setup.bash

if [ "$1" = "simple" ]; then
    echo "Starting in simple mode..."
    roslaunch robot_driver single_finger_start.launch
elif [ "$1" = "preview" ]; then
    echo "Starting with preview..."
    roslaunch robot_driver single_finger_start.launch show_preview:=true
elif [ "$1" = "serial" ] && [ -n "$2" ]; then
    echo "Starting with serial port: $2"
    roslaunch robot_driver single_finger_start.launch serial:=$2
else
    echo "Default launch..."
    echo "Options:"
    echo "  simple    - simple mode (no preview)"
    echo "  preview   - preview mode (camera windows)"
    echo "  serial /dev/ttyFingerLeft - explicit serial device"
    roslaunch robot_driver single_finger_start.launch
fi
