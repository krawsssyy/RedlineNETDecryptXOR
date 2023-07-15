import os
import re
import sys
import hashlib

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def find_key(resName, exeName):
	os.system('cmd.exe /c de4dot ' + exeName)
	os.system('cmd.exe /c del ' + exeName)
	exeName = exeName + "-cleaned"
	with open(resName, 'rb') as f:
		data = f.read(2)
	firstTwo = byte_xor(data, str.encode('MZ')).decode('utf-8')
	pattern = firstTwo + '[A-Za-z]{9}'
	os.system('cmd.exe /c strings ' + exeName + ' > strings.txt')
	with open('strings.txt', 'r') as f:
		while True:
			line = f.readline()
			if not line:
				break
			results = re.search(pattern, line)
			if results:
				decrypt(resName, results.group(0))
				break
	os.system('cmd.exe /c del strings.txt')
	os.system('cmd.exe /c del ' + resName)
	os.system('cmd.exe /c del ' + exeName)

def decrypt(resName, key):
	bytearr = []
	with open(resName, 'rb') as f:
	      while True:
	            readbyte = f.read(1)
	            if not readbyte:
	                  break
	            bytearr.append(readbyte)
	write_hashes("original", bytearr)
	for i in range(len(bytearr)):
	      bytearr[i] = byte_xor(bytearr[i], str.encode(key[i % len(key)]))
	write_hashes("decrypted", bytearr)
	with open('rsrcout.bin', 'wb') as g:
	    for byte in bytearr:
	    	g.write(byte)

def write_hashes(rsrcType, bytearr):
	print(rsrcType + " resource hash")
	strr = ""
	m = hashlib.sha256()
	for byte in bytearr:
		m.update(byte)
	print(m.hexdigest())

if __name__ == "__main__":
	find_key(sys.argv[2], sys.argv[1])