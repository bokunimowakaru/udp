#!/bin/bash
#
# fehを自動起動するには以下のコマンドを/etc/rc.localに入れておく
#
# sudo -u pi /home/pi/feh.sh delay &
#
PID=`pidof feh`
if [ "${PID}" != "" ] || [ "${1}" = "stop" ]; then
        kill $PID
fi
export DISPLAY=:0
XAUTHORITY=/home/pi/.Xauthority
if [ $# -eq 0 ] || [ "${1}" = "start" ]; then
        /usr/bin/feh -FZxYD10 /home/pi/Pictures/ &
fi
if [ "${1}" = "delay" ]; then
        sleep 30 && /usr/bin/feh -FZxYD10 /home/pi/Pictures/ &
fi
exit
