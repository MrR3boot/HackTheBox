# -*- coding: utf-8 -*-
import subprocess
import sys
import os
import re
import socket
import pexpect
from ftplib import FTP
from threading import Thread
from time import sleep

#I always love to see my script colorful with banners
print '''\033[1;31;40m
                   _                       _ __  
 __ __ __ __ _    | |__    ___    _  _    | '_ \ 
 \ V  V // _` |   | / /   / -_)  | \| |   | .__/ 
  \_/\_/ \__,_|   |_\_\   \___|   \_,_|   |_|__  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'

			\033[1;36;40mLet's Hack The Boxes \033[1;33;40mMrR3boot\033[1;32;40m
╔══╗
╚╗╔╝
╔╝(¯`v´¯)
╚══`.¸.Hacking...\033[1;37;40m'''


def portscan(ip,machine,path):
	print "\n[+] Going for port scan in background : \033[1;35;40mnmap -sV -sC -Pn -p- --max-retries=0 -oA {}/{}/nmap/scan {} >/dev/null &".format(path,machine,ip)
	subprocess.Popen(["mkdir","-p","{}/{}/nmap".format(path,machine)])
	cmd = "/usr/bin/nmap -sV -sC -p- -Pn --max-retries=0 -oA {}/{}/nmap/scan {} >/dev/null &".format(path,machine,ip)
	subprocess.call(cmd,shell=True)

def webscan(ip,machine,path):
	print "\n\033[1;37;40m[+] Checking for web related stuff"
	sleep(3)
	#To save time just check 80,443 with curl and dig in
	subprocess.Popen(["mkdir","{}/{}/web".format(path,machine)])
	p = subprocess.Popen(["curl","http://{}".format(ip)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = p.communicate()
	if stdout!="":
		print "	\033[1;32;40m[*] Port 80 is up. Going in"
		cmd = '''gobuster -np -fw -q -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://{} -x php,asp,aspx,jsp,docx,txt,zip -t 10 -o {}/{}/web/go_http >/dev/null &'''.format(ip,path,machine)
		subprocess.call(cmd,shell=True,stdout=None)
	else:
		print "	\033[1;31;40m[-] Port 80 is down. Checking SSL"
	p = subprocess.Popen(["curl","-k","https://{}".format(ip)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = p.communicate()
	if stdout!="":
		print "	\033[1;32;40m[*] Port 443 is up. Going in"
		cmd = '''gobuster -k -fw -q -np -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u https://{} -x php,asp,aspx,jsp,docx,txt,zip -t 10 -o {}/{}/web/go_https >/dev/null &'''.format(ip,path,machine)
		subprocess.call(cmd,shell=True,stdout=None)
	else:
		print "	\033[1;31;40m[-] Port 443 is down. Giving up"

def smbscan(ip,machine,path):
	print "\n\033[1;37;40m[+] Checking if OS is Win/Linux"
	cmd = """ping -c5 {} | grep -m 1 ttl | cut -d '=' -f3 | cut -d ' ' -f1""".format(ip)
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
	output,err = p.communicate()
	if output.strip("\n") != "128" and output.strip("\n") != "32" and output.strip("\n")!= "127":
		print "	\033[1;33;40m[-]It seems to be Linux. Double check if smb is open on Linux"
	else:
		creds = ['anonymous:anonymous','root:root','anonymous:""','root:""']
		for cred in creds:
			user,passwd = cred.split(":")
			cmd = '''smbmap -u {} -p {} -H {}'''.format(user,passwd,ip)
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			stdout,err = p.communicate()
			if re.search(r'Authentication error',stdout):
				print "	\033[1;31;40m[-] We don't have access to shares"
			else:
				print "	\033[1;32;40m[*] Found shares accessible using {}. Writing Results..".format(cred)
				cmd = "mkdir {}/{}/smb".format(path,machine)
				subprocess.Popen(cmd,shell=True)
				sleep(3)
				f = open("{}/{}/smb/scan-{}-{}".format(path,machine,user,passwd),"w")
				f.write(stdout)
				f.close()

def ftpscan(ip,machine,path):
	sleep(4)
	print "\n\033[1;37;40m[+] Checking if FTP is up"
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	status = s.connect_ex(('{}'.format(ip),21))
	if status == "0":
		print "	\033[1;32;40m[*] Port 21 is open. Checking anonymous access"
		sock.close()
		ftp = FTP('{}'.format(ip))
		try:
			ftp.login()
			data = []
			ftp.getwelcome(data.append)
			ftp.dir(data.append)
			ftp.quit()
			cmd = "mkdir {}/{}/ftp".format(path,machine)
			subprocess.Popen(cmd, shell=True)
			sleep(3)
			f = open("{}/{}/ftp/anon-login".format(path,machine),"w")
			for a in data:
				f.write(a)
			f.close()
		except:
			print "		\033[1;31;40m[-] Login failed."
	else:
		print "	\033[1;31;40m[-] Port 21 is closed. Double check port scan due to resets from fellow hackers.."


if __name__=="__main__":
	if len(sys.argv[1:])<2:
		print "\nUsage: python wakeup.py <machine name> <ip>\n"
	else:
		ip = sys.argv[2]
		machine = sys.argv[1]
		#Modify this line to your need.
		path = ""
		if path == "":
			print "\nPlease open the script and setup the path to store output"
		else:
			t1 = Thread(target=portscan,args=(ip,machine,path,))
			t2 = Thread(target=webscan,args=(ip,machine,path,))
			t3 = Thread(target=smbscan,args=(ip,machine,path,))
			t4 = Thread(target=ftpscan,args=(ip,machine,path,))
			t1.start()
			t2.start()
			t1.join()
			t2.join()
			t3.start()
			t3.join()
			t4.start()
			t4.join()
			#subprocess making terminal fuzzy. Reset it for normal use
			subprocess.call(["stty","sane"])
			print "\n\033[1;37;40m[*] Job Done. Check {} for results..".format("{}/".format(path) + machine)
