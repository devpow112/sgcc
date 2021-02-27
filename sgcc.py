#!/usr/bin/env python3

import argparse
import errno
import os
import shutil
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
  parser.add_argument(
    '-i',
    '--in-place',
    action="store_true",
    help="Make header change in-place, otherwise make another file"
  )
  args = parser.parse_args()
  source_path = os.path.abspath(args.path[0])
  if not os.path.isfile(source_path):
    print('ERROR: Input file is not valid or does not exist.')
    return errno.EINVAL
  if not args.in_place:
    source_path_parts = os.path.splitext(source_path)
    new_path = source_path_parts[0] + '_cc'
    destination_path = new_path + source_path_parts[1]
    shutil.copyfile(source_path, destination_path)
  else:
    destination_path = source_path
  print('Reading ROM header checksum ...')
  with open(source_path, 'rb') as source_file:
    valid_source_file = verify_console_name(source_file)
    if not valid_source_file:
      print('ERROR: File is not a valid Genesis or Mega Drive ROM file.')
      return errno.ENOTRECOVERABLE
    header_checksum = read_checksum(source_file)
    print('ROM Header checksum:', format_word(header_checksum))
    print('Computing checksum...')
    computed_checksum = compute_checksum(source_file)
    print('Computed checksum:', format_word(computed_checksum))
    if header_checksum == computed_checksum:
      print('Checksums match!')
      return 0
    print('WARNING: Checksums do not match!')
  with open(destination_path, 'r+b') as destination_file:
    print('Writing ROM header checksum ...')
    write_checksum(destination_file, computed_checksum)
    print('Verifying ROM header checksum ...')
    header_checksum = read_checksum(destination_file)
    if header_checksum == computed_checksum:
      print('Checksums match!')
      return 0
    print('ERROR: Failed to write ROM header checksum to file')
    print('Aborting script ...')
    return errno.ENOTRECOVERABLE

def format_word(word):
  return '0x{0:04X}'.format(word)

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

exit(main())
