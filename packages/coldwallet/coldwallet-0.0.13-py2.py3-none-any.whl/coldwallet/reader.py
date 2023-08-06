from __future__ import absolute_import, division, print_function

def api1(keys, api_version=1):
  '''File reading API v1.
     Bitcoin addresses are passed as a dictionary with { public-key: encrypted-exponent }.
  '''
  print("Your keys are:")
  from pprint import pprint
  pprint(keys)
  print("I don't yet know what to do from here")
