from __future__ import absolute_import, division, print_function

import argparse
import coldwallet

def main():
  print("coldwallet v%s at your service." % coldwallet.__version__)
  parser = argparse.ArgumentParser()
  parser.parse_args()
