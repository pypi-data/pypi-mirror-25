# helper functions relating to bitcoin addresses

from __future__ import absolute_import, division

import math
import re

from Crypto.Hash import SHA256

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58index = { k: n for n, k in enumerate(__b58chars) }
__b58base = len(__b58chars)

def b58decode(v, length):
  """ decode v into a string of len bytes """
  long_value = 0L
  for (i, c) in enumerate(v[::-1]):
    long_value += __b58chars.find(c) * (__b58base**i)

  result = ''
  while long_value >= 256:
    div, mod = divmod(long_value, 256)
    result = chr(mod) + result
    long_value = div
  result = chr(long_value) + result

  nPad = 0
  for c in v:
    if c == __b58chars[0]: nPad += 1
    else: break

  result = chr(0)*nPad + result
  if length is not None and len(result) != length:
    return None

  return result

def get_bcaddress_version(strAddress):
  """ Returns None if strAddress is invalid.  Otherwise returns integer version of address. """
  addr = b58decode(strAddress,25)
  if addr is None: return None
  version = addr[0]
  checksum = addr[-4:]
  vh160 = addr[:-4] # Version plus hash160 is what is checksummed
  h3=SHA256.new(SHA256.new(vh160).digest()).digest()
  if h3[0:4] == checksum:
    return ord(version)
  return None

def verify_address(value):
  value = value.strip()
  if re.match(r"[a-zA-Z1-9]{27,35}$", value) is None:
    raise RuntimeError('invalid')
  version = get_bcaddress_version(value)
  if version is None:
    raise RuntimeError('invalid')
  return value
