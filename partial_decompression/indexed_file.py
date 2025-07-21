"""

This script demonstrates two straightforward use-cases of the
indexed_bzip2 library for bzip2-compressed files:

1. Create and save a block-offset index for later random-access reads.
2. Load the index and perform a seek-and-read at an arbitrary position
   without having to decompress the entire archive.

"""

import os
import pickle
import indexed_bzip2 as ibz2
import sys

#-------------------------------------
# Path to your compressed archive
#-------------------------------------

input_bz2 = "02_HITEMP2024.par.bz2"
output_index = "CO2_indexed_offsets.dat"
bz2_file = ibz2.open(input_bz2, parallelization=os.cpu_count())
# Compute a dict mapping compressed-block-bit-offset -> uncompressed-byte-offset
block_offsets = bz2_file.block_offsets()
bz2_file.close()

with open(output_index, 'wb') as f:
    pickle.dump(block_offsets, f)

print(f"Index saved to '{output_index}'. Contains {len(block_offsets)} entries.")

# --------------------------------------------
# Load index and perform a random-access read.
# --------------------------------------------

# Load the previously saved index
with open(output_index, 'rb') as f:
    loaded_offsets = pickle.load(f)

bz2_file2 = ibz2.open("02_HITEMP2024.par.bz2", parallelization=os.cpu_count())
bz2_file2.set_block_offsets(loaded_offsets)
seek_position = 40291456000  # in bytes
bz2_file2.seek(seek_position)

length_to_read = 100  # bytes
raw_data = bz2_file2.read(length_to_read)
data = raw_data.decode('utf-8', errors='replace')
print(f"Read {len(raw_data)} bytes from position {seek_position}:\n")
print(data)
bz2_file2.close()
