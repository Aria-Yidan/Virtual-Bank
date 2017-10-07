#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
from Crypto.Cipher import AES
import base64
PADDING = '\0'
#PADDING = ' '
pad_it = lambda s: s+(16 - len(s)%16)*PADDING  
key = 'vhurVnPgi:0NA=K1'
iv = 'ZTjoHI;mLfbFaIqB'
source = 'shopid=201605062233599122$$payOrderID=201605070202266516$$payMoney=1100'
generator = AES.new(key, AES.MODE_CBC, iv)
crypt = generator.encrypt(pad_it(source))  
cryptedStr = base64.b64encode(crypt)
print cryptedStr
generator = AES.new(key, AES.MODE_CBC, iv)
recovery = generator.decrypt(crypt)
print recovery.rstrip(PADDING)


from RSA import *
#rsa_key = RSAKeyPair("10001","367fbdde3df00db317f914949dd02b01","94b8c162b498f08d139461950b4f3851")
#rsa_key = RSAKeyPair("10001","59a4d41533777950f9580b6c1bd1c78abc1a597429e27901bd475a9abeccde7450132d73224bb3747f98bec9704be7b9265bba8dba5b27a6b57fdbbdf1525881","92ec287fefb11b13c7bebab2ce2572b59961afbf2e5c8ddf185aa7184e0df5273987909aabb005d9dea46b01c1d9de0bad336363ad607679411cd8fd24ceb609")
#rsa_key = RSAKeyPair("10001","571888e7c82d94c464301df6f4aceae4cf9f3f2c264b76386a40dc259c638d4af27a5ac887c56beff418341e277683259adb733a37e635ac4b9ede183ce43931","c8cb865b331e5dbaaf204009f74374dcbae214f10041f609eda881858c3899e84b237651ea84574f452d7b9cc20a065b419908fcf70127ebf283a7168faf9fb9")

#--256 RSA_SIGHKEY--#
#rsa_sign_key = RSAKeyPair("b7016153f40bea483d5d9bbc0b4159e076ac39829a8875227b9a8476b955dbc1","10001","cdd415eb7af8136b53e982cc0a375d55d61a8b37dce44e96f4319508970612bd")
#rsa_sign_key = RSAKeyPair("71e97ed0f3aafb1866428890726f3a122a4213af794c2c35ae9421fcc4ba8111","10001","da5a203701df134c5e4e30fdb388d5dee2b3eceb5c61711e2db7cc99f21b52a3")

#--256 RSA_KEY--#
rsa_key = RSAKeyPair("10001","35cd90c8a07d6c0b321fefbaee30e385e3b222e311955edffa2d5925a17087b1","9982229e513f54e8c697fe5681a2e4f996381c21312c1f53695e20151f7ff9cb")
rsa_key = RSAKeyPair("10001","7188d3116d65cedc359676bdd0c6a56b2a578cb7e3ce11bfadc4e2f4c985fc61","88cf7808d9f31d09a0c08e48e3f4007131f331d63277442983d19740c665bd8f")

iv = "15902d7b21cf16067db3ef4bb3924b22"

#orderid = "201605062109404193"
orderid = "12345678"
#orderid = "test"
enorderid = encryptedString(rsa_key,orderid)
#enorderid = "55cab5d80522103c1cb2b00d24cac5e8818488636d519268461a43365b1c7c967ac2ba179fb3d4e5e2e8be37ab4dc0e6381ce0c4c7bf39f7a93cd0a092ee6f76"
print enorderid
#enorderid = iv
#enorderid = "19fd5cb5bde8bd119d60730426f6dd02"
orderid = decryptedString(rsa_key,enorderid)
print orderid
"""

import rsa
#import base64

rsa_key_e = "10001"
rsa_key_d = "743f9ea2f7e12fbc78271b2e054773f1de19db6256301e488d2965cdde1db72a12c3fc942eb64c7430c8c9fc8104df519a402133b48d4d5ab5c7dfdd8df71b31"
rsa_key_n = "9e1e1914b27a4b5bde2a006b9fc701ffd9fa686c9b8f06757d8d952bdea252c0b647e4720583d0f55d7355a7ae687e21b1767c195d85b8e645ddcb6eb6241d8b"
rsa_key_p = "9e4623c3607e000033730696ed69120c1a905ab480290b0e9bcecb06a6c26f300ee9"
rsa_key_q = "ffbf3c0ce0b37676980b7636041eff9a7bfc1b9b93e9ced3906a21580853"

pub = rsa.PublicKey(int(rsa_key_n,16),int(rsa_key_e,16))
pri = rsa.PrivateKey(int(rsa_key_n,16),int(rsa_key_e,16),int(rsa_key_d,16),int(rsa_key_p,16),int(rsa_key_q,16))
m = "test"
#print hex(pub.n)
#c = "51d6af999fa5f24a492645ed064f2c6e0eb23eee3784c442d8138071ee56f5d54e3122c64c0aa1f3d0b8bffc5b1fa375b738cf2f9c9bdfb53e4a736da608ea83"
#temp = ''
#for i in range(0,len(c),2):
#    temp += chr(int(c[i:i+2],16))
#c = temp

crypto1= "15f6f6d0ae2c83e43da3707105de50f7f0e4d8efcb4502b4ad91a2b8617a199336c40d843faa34db1b6b9629442b69b2e5bdb57bd63e6a9a3953f31efe20dd36"
if(len(crypto1 )% 2 == 1):
    crypto1 = '0' + crypto1
crypto = ""
for i in range(0,len(crypto1)-1,2):
    crypto += chr(int(crypto1[i] + crypto1[i+1],16))
message = rsa.decrypt(crypto, pri)
print message

#c= rsa.encrypt(m,pub)
#print c
#m1 = rsa.decrypt(c,pri)
#print m1