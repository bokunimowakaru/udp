#!/bin/bash

# オーバレイモードのドライブの存在を確認し、プロンプトを変更します。
# 使用方法: source ~/udp/udp_monitor/olCheck.sh

echo "Usage: source" $0 
i=`df|grep "^overlay"| tail -1`
if [ "$i" = "" ]; then
	PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w \$\[\033[00m\] '
	echo "unlocked"
else
	PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[01;31m\](LOCKED)\[\033[00m\]:\[\033[01;34m\]\w \$\[\033[00m\] '
	echo "Locked"
fi
