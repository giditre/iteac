#!/bin/bash

screen -dmS iteac bash -c 'cd; bash'
screen -S iteac -X  'chdir'

screen -S iteac -X screen -t main bash -c 'cd /home/pi/iteac; bash'
screen -S iteac -p main -X stuff 'python3 main.py || sudo halt^M'

