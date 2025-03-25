# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:44:45 2025

@author: dcmvd
"""

import numpy as np
from mypath import fpath
import bz2

i_min, i_max = 1, 3

fname = fpath + '02_HITEMP2024.par.bz2'
sname = 'db/db_subset.txt'

offsets, pads = np.load('offset_arr.npy')
sizes = offsets[1:] - offsets[:-1]

header = b'BZh91AY&SY'
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


# Read blocks:
with open(fname, 'rb') as fr:
    fr.seek(offsets[i_min])
    buf = fr.read(offsets[i_max + 1] - offsets[i_min] + 10)

# Decompress blocks:
with open(sname, 'wb') as fw:
    
    # write alignment block:
    decomp = bz2.BZ2Decompressor()
    decomp.decompress(header + pad_bufs[pads[i_min]])
            
    # write data block:
    data = decomp.decompress(buf)
    fw.write(data)
    decomp = None

print('Done!')