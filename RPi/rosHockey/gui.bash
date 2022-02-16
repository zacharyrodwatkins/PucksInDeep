#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
#source /opt/ros/foxy/setup.bash
source $SCRIPT_DIR/install/local_setup.bash
if  ! ros2 node list | grep -q bp_coms ; then
	ros2 run bp_coms_cpp bp_coms
fi

python3 $SCRIPT_DIR/hockey_gui/hockey_gui/main.py
