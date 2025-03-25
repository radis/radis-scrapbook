# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:44:45 2025

@author: dcmvd
"""

import numpy as np
from mypath import fpath
import bz2

fname = fpath + '02_HITEMP2024.par.bz2'
sname = 'db/db_subset.txt'

offsets, pads = np.load('offset_arr.npy')
sizes = offsets[1:] - offsets[:-1]
N = len(offsets) - 1

def merge_bytes(byte1, byte2, pad):
    mask = 0xff << pad
    return int((byte1 & mask) | (byte2 & (~mask))).to_bytes(1)
    

stream_header = b'BZh9'
block_magic = b'1AY&SY'
pad_bufs = [
	b' Q\xb2\x1c\x00\x00\x03Z\x00\x00\x10\x0c\x00@\x00\x00\n \x000\xc0\x084\xf2 b\xfd',
	b'\x89\xbf\xa3\xf5\x00\x00\x03Z\x00\x00\x10\x0e\x00 \x00\x00\n \x001\x0c\x01\x06\x99\xa1?\x19\n',
	b'Y\x9e\xb7A\x00\x00\x03Z\x00\x00\x10\x0c\x00\x10\x00\x00\n \x000\xc0\x08a\xa1gPx',
	b'\x13\xc2\x98\xc5\x00\x00\x03Z\x00\x00\x10\x0c\x00\x08\x00\x00\n \x000\xc0\x08a\xa1e@\xf1',
	b'\xe7%cn\x00\x00\x03\xda\x00@\x10\x08\x00\x04\x00\x00\n \x00"\x18h0\x06/\xa0c',
	b'm\x96(6\x00\x00\x03Z\x00\x00\x10\x0e\x00\x02\x00\x00\n \x001\x0c\x01\x01\xb2\x89\xc6#\xe6',
	b'|\x80\xf4\xd9\x00\x00\x03Z\x00\x00\x10\x0c\x00\x01\x00\x00\n \x00"\x18h0\x02\xcf)\x8c',
	b'\xc9\xec\x1b[\x00\x00\x03Z\x00\x00\x10\x0e\x00\x00\x80\x00\n \x001\x0c\x01\r1\xa8Y0\xa7\x98',
    ]


decomp = bz2.BZ2Decompressor()
init = None
with open(fname, 'rb') as fr, open(sname, 'wb') as fw:
    for i in [1,2,3]:

        print(i, offsets[i], pads[i])
        
        # write alignment block:
        if init is None:
            init = decomp.decompress(stream_header + block_magic + pad_bufs[pads[i]])
            fr.seek(offsets[i])

        # write data block:
        buf = fr.read(sizes[i])
        data = decomp.decompress(buf)
        fw.write(data)

    # Append the header of the next block to trigger decompression of the last block:
    buf = fr.read(10)
    data = decomp.decompress(buf)
    fw.write(data)
    
print('Done!')