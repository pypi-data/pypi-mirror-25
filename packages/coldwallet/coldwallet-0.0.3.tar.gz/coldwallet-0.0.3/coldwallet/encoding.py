# helper functions for shuffling bits around various formats

from __future__ import absolute_import, division

import binascii
import hashlib
import struct

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58index = { k: n for n, k in enumerate(__b58chars) }

def base58_decode(b58):
  '''Take a base58 encoded string and return the represented value as an integer.'''
  value = 0
  for c in b58:
    value = value * 58 + __b58index[c]
  return value

def base58_encode(value):
  '''Take an integer and return the shortest base58 encoded string representation.'''
  b58 = ''
  while value > 0:
    b58 = __b58chars[value % 58] + b58
    value = value // 58
  return b58

def _get_5bit_checksum(value):
  '''Take an unsigned 64-bit integer and return an unsigned 5-bit checksum.
     The checksum is calculated by running SHA256 on the integer and extracting
     the five leading bits of the resulting hash.'''
  # Convert the number to an 8 byte string and run SHA256
  checksumhash = hashlib.sha256(struct.pack('<Q', value)).digest()
  # Extract the five most significant bits of the first byte
  return ord(checksumhash[0:1]) >> 3

def block7_encode(value):
  '''Take an integer < 2^36 (36 bits worth of data), add a 5 bit checksum, and
     return a 7 character base58 encoded string (41 bits worth of data).
     The checksum is used purely to guard against accidental mistyping of the
     code block. It is not relevant from a cryptographical perspective.
  '''
  # The checksum is calculated by treating the passed integer as a 64-bit value,
  # running SHA256 and extracting the five leading bits of the resulting hash.
  checksum = _get_5bit_checksum(value)

  # The 5 checksum bits are appended (as LSB) to the 36 data bits. This results
  # in a 41 bit value, which fits the 7 character base 58 block nearly exactly:
  #    2^41 = 2 199 023 255 552 < 2 207 984 167 552 = 58^7
  block7 = base58_encode((value << 5) + checksum)

  # blocks shorter than 7 characters (= values < 58^6 / 32 = 1 189 646 642) are
  # prefixed with leading '1's to reach 7 characters.
  block7 = '1' * (7 - len(block7)) + block7

  return block7

def block7_decode(block7):
  '''Take a 7 character base58 encoded string (41 bits), separate into data
     and checksum, verify said checksum, and return a dictionary containing
     an unsigned integer representation of the data portion, and a boolean
     indicating whether the checksum was valid or not.
  '''
  # Decode and split numeric value into data and checksum
  value = base58_decode(block7)
  checksum = value & 0b00011111
  value = value >> 5

  # Calculate the expected checksum for the data portion, see block7_encode().
  expchecksum = _get_5bit_checksum(value)

  return { 'value': value, \
           'valid': checksum == expchecksum }

def crc8(data):
  '''Generate an 8 bit non-cryptographical checksum for any string.
     This is used only for direct user feedback to avoid input errors.
  '''
  return "%02x" % (binascii.crc32(bytearray(data, 'ascii')) & 0xff)
