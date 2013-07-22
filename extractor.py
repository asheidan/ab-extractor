#!/usr/bin/env python

import fileinput
import sys
import zlib

BLOCK_SIZE = 10 * (1024 ** 2)

def si(number):
    SUFFIXES = ['','k','M','G','T']
    SU_STEP = 1024.0

    while number > SU_STEP:
        number /= SU_STEP
        del SUFFIXES[0]

    return "%.1f%s    " % (number, SUFFIXES[0])

input_filename = sys.argv[1]
input_file = open(input_filename, "rb")

magic_line = input_file.readline().strip()
backup_version = input_file.readline().strip()
compressed = input_file.readline().strip() == '1'
encryption = input_file.readline().strip()

suffix = ['tar']

if not encryption is "none":
    # the "user password salt" encoded in hex, all caps
    # the "master key checksum salt" encoded in hex, all caps
    # the "number of PBKDF2 rounds used" as a decimal number
    # the "IV of the user key" encoded in hex, all caps
    # the "master IV + key blob, encrypted by the user key" encoded in hex, all caps
    pass

if compressed is True:
    suffix.append('gz')

print "Magic:      ", magic_line
print "Format:     ", backup_version
print "Compressed: ", compressed
print "Encryption: ", encryption

#The actual backup data follows, either as (depending on compression and encryption) tar, deflate(tar), encrypt(tar), or encrypt(deflate(tar)).

output_filename = '.'.join(['datadump'] + suffix)

print "Output file:", output_filename

read_data_size = 0
write_data_size = 0
last_read_size = 2 ** 30
last_read_size = 2 ** 30

decompressor = zlib.decompressobj(-15)

with open(output_filename, 'wb') as output_file:
    while 0 < last_read_size:
        deflated_data = input_file.read(BLOCK_SIZE)
        last_read_size = len(deflated_data)
        read_data_size += last_read_size

        inflated_data = decompressor.decompress(deflated_data)
        write_data_size += len(inflated_data)
        output_file.write(inflated_data)

        sys.stderr.write("\rRead: %s / Write: s\r" % (si(read_data_size),si(write_data_size)))

input_file.close()
