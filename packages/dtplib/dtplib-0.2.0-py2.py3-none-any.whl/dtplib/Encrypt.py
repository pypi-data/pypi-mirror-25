"""Encryption functions. Useful for network servers.

Example:
    >>> from dtplib.Encrypt import encrypt, decrypt, random
    >>> key = "this is a key123"
    >>> IV = "this is an IV456"
    >>> message = "Hello World!"
    >>> message
    'Hello World!'
    >>> e = encrypt(message, key, IV)
    >>> e
    '\x00\xc8\x88\xe9=\x93\xa4`i\x86\xfb\xe5n\xd2<`'
    >>> d = decrypt(e, key, IV)
    >>> d
    'Hello World!'
    >>> d == message
    True
    >>> random()
    'f\x96\xbaJ\x93>\x89;R(n \x80\xcd\xa2\xb9'
    >>> random(4)
    '\xb2\xc2M\xb4'
"""

from Crypto.Cipher import AES
from Crypto import Random

def encrypt(text, key, IV):
    """Encrypt text of any length with a key and IV."""
    rndfile = Random.new()
    extra = 15 - (len(text) % 16)
    text = chr(extra + 1) + rndfile.read(extra) + text
    rndfile.close()
    obj = AES.new(key, AES.MODE_CBC, IV)
    text = obj.encrypt(text)
    return text

def decrypt(text, key, IV):
    """Decrypt text with a key and IV."""
    obj = AES.new(key, AES.MODE_CBC, IV)
    text = obj.decrypt(text)
    return text[ord(text[0]):]

def random(length = 16):
    """Generate a random key or IV."""
    rndfile = Random.new()
    text = rndfile.read(length)
    rndfile.close()
    return text

if __name__ == "__main__":
    pass
