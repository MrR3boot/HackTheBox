import random 
import json
import hashlib
import binascii
from ecdsa import VerifyingKey, SigningKey, NIST384p
from bottle import route, run, request, debug
from bottle import hook
from bottle import response as resp


def secure_rng(seed): 
    # Taken from the internet - probably secure
    p = 2147483647
    g = 2255412

    keyLength = 32
    ret = 0
    ths = round((p-1)/2)
    for i in range(keyLength*8):
        seed = pow(g,seed,p)
        if seed > ths:
            ret += 2**i
    return ret

# Set up the keys
with open('out.txt','a') as f:
	for _ in range(20000):
		seed = random.getrandbits(128)
		rand = secure_rng(seed)
		f.write(str(rand)+'\n')
f.close()
