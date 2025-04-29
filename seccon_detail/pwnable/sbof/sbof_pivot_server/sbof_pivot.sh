#!/bin/bash

# [rp++ install]
# sudo apt update
# sudo apt install cmake ninja-build
# chmod u+x ./build-release.sh && ./build-release.sh
#
# git clone https://github.com/0vercl0k/rp
# cd rp/
# cd src/build/
# chmod u+x ./build-release.sh && ./build-release.sh

gcc sbof_pivot.c tcp_server.c -fno-stack-protector -no-pie -g -o sbof_pivot

nm sbof_pivot | grep msg
nm sbof_pivot | grep win

$HOME/git/rp/src/build/rp-lin -f sbof_pivot -r 5 --unique --print-bytes  | sed -r 's/\x1b\[[0-9]+m//g' | grep -e ": pop rsp" -e ": leave"
$HOME/git/rp/src/build/rp-lin -f sbof_pivot -r 5 --unique --print-bytes  | grep -A 1 "pop rdi"
$HOME/git/rp/src/build/rp-lin -f sbof_pivot -r 5 --unique --print-bytes  | grep -A 1 "pop rsi"

./sbof_pivot
