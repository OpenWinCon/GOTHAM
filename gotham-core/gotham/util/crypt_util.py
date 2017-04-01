# encoding: utf-8

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto import Random

import os

__author__ = 'BetaS'


def generateKey():
    random_generator = Random.new().read
    privatekey = RSA.generate(1024, random_generator)
    publickey = privatekey.publickey()

    f = open("private.key", "wb")
    f.write(privatekey.exportKey('DER'))
    f.close()

    f = open("public.key", "wb")
    f.write(publickey.exportKey('DER'))
    f.close()


def sign(data):
    if not (os.path.isfile("public.key") and os.path.isfile("private.key")):
        print("[!] Key has not generated")
        generateKey()

    # Signing file
    f = open("private.key", 'rb')
    key = RSA.importKey(f.read())
    signer = PKCS1_v1_5.new(key)
    hash = SHA512.new(data)
    s = signer.sign(hash)

    f.close()

    return s


def verify(data, sign):
    if not (os.path.isfile("public.key") and os.path.isfile("private.key")):
        print("[!] Key has not generated")
        generateKey()

    f = open("public.key", 'rb')
    key = RSA.importKey(f.read())
    signer = PKCS1_v1_5.new(key)
    hash = SHA512.new(data)
    f.close()

    return signer.verify(hash, sign)
