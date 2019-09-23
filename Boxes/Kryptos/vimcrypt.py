with open('creds.txt','rb') as f:
	f.seek(28)
	a = bytearray('rijndael')
	b = bytearray(f.read(8))
	c = bytearray(len(a))
	for i in range(len(a)):
		c[i] = a[i] ^ b[i]
	#1st block
	a = bytearray(len(a))
	for i in range(len(a)):
		a[i] = c[i] ^ b[i]
	print a
	#2nd block
	b = bytearray(f.read(8))
	a = bytearray(len(a))
	for i in range(len(a)):
		a[i] = c[i] ^ b[i]
	print a

	#3rd block
	b = bytearray(f.read(8))
	a = bytearray(len(a))
	for i in range(0,len(a)):
		a[i] = c[i] ^ b[i]
	print a

	#4th block
	b = bytearray(f.read(8))
	a = bytearray(len(a))
	for i in range(len(a)):
		a[i] = c[i] ^ b[i]
	print a
