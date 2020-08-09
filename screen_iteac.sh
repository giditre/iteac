#!/bin/bash

screen -dmS iteac bash -c 'cd; bash'
screen -S iteac -X  'chdir'

screen -S iteac -X screen -t 7seg bash -c 'cd /home/pi/iteac; bash'
#screen -S forchdev -p UA -X stuff "vim forch_user_access.py"

screen -S iteac -X screen -t git bash -c 'cd /home/pi/iteac; bash'
screen -S iteac -p git -X stuff 'git pull && git add -A && git commit -a -m "commit from $(hostname) on $(date)" && git push^M'
