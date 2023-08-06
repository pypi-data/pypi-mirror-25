# AES crypto functions: encryption and decryption

from __future__ import absolute_import, division

import hashlib
import os

from Cryptodome.Cipher import AES

def encrypt_block(data, key, iv=None):
  '''AES256 encrypt a string with a given key. There is no padding mechanism,
     so the data must be given as a multiple of 128 bits. A 128 bit initializion
     vector may be specified, and is randomly generated otherwise.
  '''
  assert len(key) == 32, 'AES encryption key must be 256 bit'
  assert data, 'No data given to encrypt'
  assert len(data) % 16 == 0, 'AES encryption data must be a multiple of 128 bit'

  # Generate a random initialization vector if none was specified.
  if iv is None:
    # Do not simpy generate a random string, for example with os.urandom(16),
    # and use it directly. The IV is stored in plain text next to the encrypted
    # message. Since the encryption key itself was generated from random number
    # shortly before generating the IV the IV may potentially leak information
    # about the PRNG state, from which an inference may be drawn about the PRNG
    # state before key generation. To avoid this the IV is drawn from a trapdoor
    # function fed with a random string instead.
    iv = hashlib.sha256(os.urandom(32)).digest()[:AES.block_size]
  assert len(iv) == AES.block_size, \
      'Initialization vector must be %d bytes' % AES.block_size

  # Prefix AES256 CBC encrypted data with plain text IV
  cipher = AES.new(key, AES.MODE_CBC, iv)
  return iv + cipher.encrypt(data)

def decrypt_block(data, key):
  '''AES256 decrypt a string with a given key. Again, no unpadding is performed.
     There is also no HMAC verification. This does not matter however as the
     decrypted output is treated as the uncompressed secret key to a bitcoin
     address. To verify message integrity we only need to compare the resulting
     public bitcoin address to the known public address.
  '''
  assert len(key) == 32, 'AES encryption key must be 256 bit'
  assert data, 'No data given to decrypt'
  assert len(data) % 16 == 0, 'AES encryption data must be a multiple of 128 bit'

  # Separate the IV from the encrypted data
  iv = data[0:AES.block_size]
  data = data[AES.block_size:]

  # Decrypt the data
  cipher = AES.new(key, AES.MODE_CBC, iv)
  return cipher.decrypt(data)
