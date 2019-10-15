# Kryptos:

## Description:
A very hard and awesome machine which involves several cryptography concepts where i'm mostly interested in.

## Walkthrough:
### User:
1. Simple Web login which has hidden ``db`` param and by poking it with certain special characters i ended up in finding a ``PDO Exception`` with ``;`` character.
2. Which shows that i can redirect target server to authenticate to my own MySQL server and can bypass authentication by creating same table and with any username/password combo.
3. We welcomed with a page which fetches remote url content and encrypts with ``AES-CBC or RC4``.
4. As we know ``RC4`` is a Stream Cipher with known vulnerabilities. So i've choosen it for fetching local files.

> As an example i've sent my local ip to fetch ``A sample text`` and it does returned with encrypted content.

> ``A (A Sample Text) XOR B (Key on server) = C (Cipher Text)``. 

> To get plaintext back we can simply send Cipher Text (C) to server which does XOR with Key (B) and can give plaintext (A) back to us.

5. Using this solution i've started fetching ``dev`` folder default file ``index.php`` content.
6. It does have ``?page=`` which immediately triggers a Local File Inclusion vulnerability. So using a php wrapper i've read ``todo`` page source which told about ``sqlitestpage`` reading its source i've identified a SQL injection writing/reading files from the server. I've automated all of above steps in [kryptos.py](https://github.com/MrR3boot/HackTheBox/blob/master/Boxes/Kryptos/kryptos.py).
7. I could see old credentials and new ``creds.txt`` on user home folder. But new credentials are encrypted with VimCrypt which uses blowfish algorigthm. It has known weakness with which we can perform ``Known Plaintext Attack`` [https://dgl.cx/2014/10/vim-blowfish].
8. Using the script [vimcrypt.py](https://github.com/MrR3boot/HackTheBox/blob/master/Boxes/Kryptos/vimcrypt.py) i've decrypted the credentials and SSHed in.

### Root:
1. On user home i've found [server.py](https://github.com/MrR3boot/HackTheBox/blob/master/Boxes/Kryptos/server.py) and by just looking at ``eval`` usage i figured out there is a way to execute our code on server as root.
2. It seems that there is signature validation against the expression that is being evaluated. But the problem is when we generate seeds they do repeat after several iterations which seems to be an issue. So i've generated seeds and kept it on file using [seed.py](https://github.com/MrR3boot/HackTheBox/blob/master/Boxes/Kryptos/seed.py).
3. Crafted a script to create signatures using generated seeds and bruteforce the server with sample expression ``3+3`` [root-exploit.py](https://github.com/MrR3boot/HackTheBox/blob/master/Boxes/Kryptos/root-exploit.py)
4. After several iterations i do see success message with evaluated expression. Then using known python sandbox bypasses i've crafted a working payload to read root.txt

## References:
1. https://crypto.stackexchange.com/questions/45021/rc4-finding-key-if-we-know-plain-text-and-ciphertext
2. https://dgl.cx/2014/10/vim-blowfish
3. https://romailler.ch/2017/11/17/ynot17-sms/
4. https://wapiflapi.github.io/2013/04/22/plaidctf-pyjail-story-of-pythons-escape
