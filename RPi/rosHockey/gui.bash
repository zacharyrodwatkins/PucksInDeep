#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source /opt/ros/foxy/setup.bash
source $SCRIPT_DIR/install/local_setup.bash
ros2 run bp_coms bp_rx & 
ros2 run bp_coms bp_tx &
python3 $SCRIPT_DIR/hockey_gui/hockey_gui/main.py
