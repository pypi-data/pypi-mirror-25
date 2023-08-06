from __future__ import absolute_import, division, print_function

import argparse
import sys

import coldwallet
import coldwallet.bitcoin
import coldwallet.crypto
import coldwallet.encoding

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--disable-randomness", help=argparse.SUPPRESS, action="store_true")
  parser.add_argument("--version", help="show version and exit", action="store_true")
  parser.add_argument("--addresses", type=int, default=4, help="generate this many bitcoin addresses")
  parser.add_argument("--codes", type=int, default=8, help="the number of code blocks used for the cold wallet")

  args = parser.parse_args()

  if args.disable_randomness:
    coldwallet.crypto.disable_randomness()

  if args.version:
    print("coldwallet v%s" % coldwallet.__version__)
    sys.exit(0)

  if args.codes < 2:
    print("The minimum number of code blocks is 2. The recommended minimum is 8.")
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
  for n in range(args.addresses):
    private_key = coldwallet.crypto.generate_random_string(bits=256)
    public_address = coldwallet.bitcoin.generate_public_address(private_key)

    print("  %s" % public_address)
    key_code = coldwallet.crypto.encrypt_secret_key(private_key, coldkey, public_address)
    print("    :%s" % key_code)
