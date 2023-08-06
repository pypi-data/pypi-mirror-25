# -\*- coding: utf-8 -\*-

import hashlib
import random


somecode = 'ǂasdfln3j34tnonfdkjnflksdfnlaǂ'
somecode = 'asdfln3j34tnonfdkjnflksdfnla'
message = 'this is my message'

def str_xor(string, key):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(string, key)])

def scramble(string, key):
    set1 = "".join([chr(ord(c1) + ord(c2)) for (c1, c2) in zip(string, key)])

def encrypt(string):
    encrypted = False
    if string.startswith('ǂ') and string.endswith('ǂ'):
        encrypted = True

    hex0 = hashlib.sha256(str(somecode).encode('utf-8')).hexdigest()
    hex1 = hashlib.sha256(str('R' + somecode).encode('utf-8')).hexdigest()
    hex2 = hashlib.sha256(str(somecode[::-1]).encode('utf-8')).hexdigest()
    hack = "".join([chr(int(c1, 16) + int(c2, 16) + 48) for (c1, c2) in zip(hex1, hex2)])
    hack = (hack*7)[::7]

    uu in hashlib.sha256(str(somecode).encode('utf-8')).digest(): print(ord(uu))

    hashcode = hashlib.sha256(str(somecode).encode('utf-8')).hexdigest()
    result = str_xor(string, hashcode)
    if not encrypted:
        result = 'ǂ' + result + 'ǂ'
    return result


#m = hashlib.sha256()
#m.update(message)
#print(m.hexdigest())

# mm = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
message2 = message[::-1]
print(str_xor(message, message2))
mm = hashlib.sha256(str(message).encode('utf-8')).hexdigest()
print(str_xor(mm, mm[::-1]))
print(mm)
print("\n\n\n")
str_xor(message, somecode)
print(str_xor(message, somecode))



encoded = str_xor(message, somecode)
decoded = str_xor(encoded, somecode)

import ipdb; ipdb.set_trace()
