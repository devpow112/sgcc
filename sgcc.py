#!/usr/bin/env python3

import argparse
import os
import struct

CHECKSUM_HEADER_OFFSET = 0x18E

def main():
  parser = argparse.ArgumentParser(
    description = 'Compares and corrects the checksum for a Sega Genesis ROM.'
  )
  parser.add_argument(
    'path',
    nargs = 1,
    help = 'Relative path to the Sega Genesis ROM file.'
  )
  args = parser.parse_args()
  print('Reading checksum from file...')
  with open(args.path[0], 'r+b') as genesis_file:
    valid_genesis_file = verify_console_name(genesis_file)
    if not valid_genesis_file:
      print('\nERROR: File is not a valid Genesis or Mega Drive ROM file.')
      return
    header_checksum = read_checksum(genesis_file)
    print('Header checksum =',)
    print_word(header_checksum)
    print('Computing checksum...')
    computed_checksum = compute_checksum(genesis_file)
    print('Computed checksum = ',)
    print_word(computed_checksum)
    if header_checksum == computed_checksum:
      print('\nChecksums match!')
      return
    print('\nWARNING: Checksums do not match!')
    print('\nWriting computed checksum to header...')
    write_checksum(genesis_file, computed_checksum)
    print('Writing complete. The header should now be updated.')
    print('Verifying header checksum...')
    header_checksum = read_checksum(genesis_file)
    if header_checksum == computed_checksum:
      print('\nChecksums match!')
      return
    print('\nERROR: Failed to write to file')
    print('Aborting script...')
    return

def print_word(word):
  print('0x{0:04X}'.format(word))

def read_byte_as_int(open_file):
  return ord(open_file.read(1))

def read_word_as_int(open_file):
  high_bits = read_byte_as_int(open_file) << 8
  low_bits = read_byte_as_int(open_file)
  return high_bits | low_bits

def read_checksum(open_file):
  open_file.seek(CHECKSUM_HEADER_OFFSET)
  return read_word_as_int(open_file)

def verify_console_name(open_file):
  memorybuffer = open_file.read()
  console_name = memorybuffer[0x100:0x110].decode('utf-8')
  if console_name.strip() == "SEGA MEGA DRIVE":
    return True
  if console_name.strip() == "SEGA GENESIS":
    return True
  if console_name.strip() == "SEGA SSF":
    return True
  return False

def compute_checksum(open_file):
  CHECKSUM_CALCULATION_START_OFFSET = 0x200
  open_file.seek(CHECKSUM_CALCULATION_START_OFFSET)
  checksum = 0
  file_size = os.path.getsize(open_file.name)
  NUM_BYTES_PER_WORD = 2
  for i in range(open_file.tell(), file_size, NUM_BYTES_PER_WORD):
    word = read_word_as_int(open_file)
    checksum += word
  WORD_MASK = 65535
  return checksum & WORD_MASK

def write_checksum(open_file, checksum):
  open_file.seek(CHECKSUM_HEADER_OFFSET)
  open_file.write(struct.pack('>H', checksum))

main()
