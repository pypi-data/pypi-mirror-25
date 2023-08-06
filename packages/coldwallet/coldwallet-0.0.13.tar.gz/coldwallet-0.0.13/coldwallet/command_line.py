from __future__ import absolute_import, division, print_function

import argparse
import json
import os
import stat
import sys

import coldwallet
import coldwallet.bitcoin
import coldwallet.crypto
import coldwallet.encoding

def main():
  '''This is the main entry point of the coldwallet generating code.
     This is what is run when you type
       coldwallet
     on the command line.

     Here we offer the user options to generate cold wallets.
  '''
  parser = argparse.ArgumentParser()
  parser.add_argument("--version", help="show version and exit", action="store_true")
  parser.add_argument("-o", "--output", default="coldwallet.py", help="write wallet file to this location (default: coldwallet.py)")
  parser.add_argument("--addresses", type=int, default=10, help="generate this many bitcoin addresses")
  parser.add_argument("--codes", type=int, default=8, help="the number of code blocks used for the cold wallet")

  # advanced parameters:

  # Disable all random number generation, making coldwallet deterministic.
  # Never use this outside of testing.
  parser.add_argument("--disable-randomness", help=argparse.SUPPRESS, action="store_true")

  # Use this power of two as the N parameter of the scrypt hashing algorithm.
  # The scrypt default is 2^14. This increases the memory requirements for
  # de- and encryption of the private keys.
  parser.add_argument("--scrypt-N", type=int, default=14, help=argparse.SUPPRESS)

  # Parse command line arguments
  args = parser.parse_args()

  if args.disable_randomness:
    coldwallet.crypto.disable_randomness()

  if args.version:
    print("coldwallet v%s" % coldwallet.__version__)
    sys.exit(0)

  if args.codes < 2:
    print("The minimum number of code blocks is 2. The recommended minimum is 8.", file=sys.stderr)
    sys.exit(1)

  if os.path.exists(args.output):
    print("Output file %s already exists. Please specify a different name." % args.output, file=sys.stderr)
    sys.exit(1)

  # Step 1. Create a coldwallet key. This key is encoded in human-readable form
  #         in blocks of 7 characters, which can be written down on paper.
  print("Generating coldwallet blocks:")
  coldkey = coldwallet.crypto.generate_random_string(bits = 36 * args.codes)
  blocks = coldwallet.encoding.block7_split(coldkey)
  assert len(blocks) == args.codes, "block count mismatch"

  for n, block in enumerate(blocks):
    verification = coldwallet.encoding.crc8(block)
    print("  %d. %s [%s]" % (n+1, block, verification))
  print("")

  # Step 1b. Verify that the key can be recreated from the blocks
  verifykey = coldwallet.encoding.block7_merge(blocks)
  assert verifykey['key'] == coldkey, "key validation error"
  assert verifykey['valid'], "key validation error"

  # Step 2.  Generate Bitcoin addresses
  print("Generating Bitcoin addresses:")
  bitcoin_addresses = {}
  for n in range(args.addresses):
    private_key = coldwallet.crypto.generate_random_string(bits=256)
    public_address = coldwallet.bitcoin.generate_public_address(private_key)

    print("  %s" % public_address)
    key_code = coldwallet.crypto.encrypt_secret_key(private_key, coldkey, public_address, scrypt_N=2**args.scrypt_N)

    verify_key = coldwallet.crypto.decrypt_secret_key(key_code, coldkey, public_address, scrypt_N=2**args.scrypt_N)
    assert private_key == verify_key, "key validation error"

    bitcoin_addresses[public_address] = key_code

  print()
  print("Generating %s" % args.output)
  with open(args.output, 'w') as fh:
    fh.write(generate_file(bitcoin_addresses))

    # set file as executable for all with read permissions
    mode = os.fstat(fh.fileno()).st_mode
    mode |= (mode & 0o444) >> 2
    os.fchmod(fh.fileno(), stat.S_IMODE(mode))

def generate_file(keys):
  '''Generate a python file containing the public bitcoin addresses and the
     encrypted secret keys.
  '''

  template = '''
#!/usr/bin/env python

if __name__ == '__main__':
  import coldwallet

  coldwallet.run(
    {keys},
    api_version=1,
  )
'''

  formatted_keys = json.dumps(keys, sort_keys=True, indent=2, separators=(',', ': ')).replace('\n', '\n    ')
  template = template.format(keys=formatted_keys)
  return template.lstrip()
