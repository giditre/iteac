#!/bin/bash

screen -dmS iteac bash -c 'cd /home/pi/iteac; bash'
screen -S iteac -X  'chdir'

screen -S iteac -X screen -t main bash -c 'cd /home/pi/iteac; bash'
screen -S iteac -p main -X stuff 'sudo pigpiod; git pull; python3 main.py; if [[ "$?" == "57" ]]; then sudo halt; fi^M'

