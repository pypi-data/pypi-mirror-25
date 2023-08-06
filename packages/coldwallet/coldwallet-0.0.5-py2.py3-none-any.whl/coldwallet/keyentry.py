from __future__ import absolute_import, division

import hashlib
import struct

def generate_entry_block_checksum(number):
  '''Calculate 5 bit verification code for a 36 bit number.'''
  assert number < (2**36), 'cannot calculate verification code for a >36 bit number'
  s = hashlib.sha256()

  # calculate the SHA256 hash value of the entry bock padded to 64 bits by appending '0's.
  s.update(struct.pack('<Q', number))

  # Extract leading 5 bits from hash
  t = struct.unpack('<B', s.digest()[0:1])[0]
  return (t & 0b11111000) >> 3
