# Coldwallet encryption related functions. This is the heart of coldwallet.

from __future__ import absolute_import, division

import base64
import math
import os

import coldwallet.aes
import pylibscrypt

def disable_randomness():
  '''Make the random number generator produce deterministic (ie. non-random)
     output. This is used for internal testing only, and must never be used
     otherwise! A warning is printed.
  '''
  import random
  import sys
  sys.stderr.write('\n-- coldwallet running in test mode - random number generation disabled --\n\n')
  def fakerandom(b):
    # bytes/bytearray conversion and use and rounding of
    # random.random() is required for Python2/3 compatibility.
    return bytes(bytearray((int(round(random.random(), 10) * 256) for x in range(b))))
  if sys.hexversion >= 0x03000000:
    random.seed(a=0, version=1)
  else:
    random.seed(a=0)
  os.urandom = fakerandom

def generate_random_string(bits):
  '''Generate a random string with a given number of bits. If the number of bits is
     not divisible by 8 then pad with 0s.
  '''
  assert bits >= 1, "Cannot create 0 bit random strings"

  stringbytes = int(math.ceil(bits / 8))
  rand_string = os.urandom(stringbytes)

  zero_padding = stringbytes * 8 - bits
  if zero_padding:
    mask = 0x100 - (2 ** zero_padding)
    rand_string = rand_string[:-1] + bytes(bytearray((ord(rand_string[-1:]) & mask,)))

  return rand_string

def encrypt_secret_key(secret, coldkey, public_address, scrypt_N=2**14, scrypt_p=1):
  '''Encrypt a secret exponent using an individual symmetric key. The symmetric
     key is generated from the shared coldwallet key (given as byte string) and
     the public bitcoin address (given in human readable format) using the
     memory-hard scrypt hash. The result is returned in base64 encoding.
  '''
  # Generate a 256 bit symmetric key from the coldwallet key and the public bitcoin address
  symmetric_key = pylibscrypt.scrypt(coldkey, public_address.encode('ascii'), olen=32, N=scrypt_N, p=scrypt_p)

  # Encrypt the secret exponent with the symmetric key
  encrypted_secret = coldwallet.aes.encrypt_block(secret, symmetric_key)

  # Base64 encode the result
  return base64.b64encode(encrypted_secret).decode('ascii')

def decrypt_secret_key(code, coldkey, public_address, scrypt_N=2**14, scrypt_p=1):
  '''Decrypt a secret exponent, given in base64 encoding, using an individual
     symmetric key. The symmetric key is generated as above. The result is
     returned as a byte string.
  '''
  # Base64 decode the input
  code = base64.b64decode(code.encode('ascii'))

  # Generate a 256 bit symmetric key from the coldwallet key and the public bitcoin address
  symmetric_key = pylibscrypt.scrypt(coldkey, public_address.encode('ascii'), olen=32, N=scrypt_N, p=scrypt_p)

  # Decrypt the secret exponent with the symmetric key
  secret = coldwallet.aes.decrypt_block(code, symmetric_key)

  return secret
