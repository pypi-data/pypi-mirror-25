#!/usr/bin/env python
# -*- coding: utf-8 -*-


import base64
import binascii
import hashlib

data=base64.decodebytes('yTDuayk5ABcJBgYyEQAAAAAAAAAEkwjQcU+u5ZHwIhQJCQvLfL1Q'.encode())
print(binascii.hexlify(data))

req = binascii.unhexlify('c930ee6b29390017090606321100000000000000049308')
# req += binascii.unhexlify('161205114500')

string = '7458d973f9124680'.encode('utf-8') + req

unsign = string[0:56]

if len(unsign) < 56:
    unsign += bytes(56 - len(unsign))

md5 = hashlib.md5(unsign).digest()
print(binascii.hexlify(md5))