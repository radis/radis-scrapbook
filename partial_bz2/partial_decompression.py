# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:44:45 2025

@author: dcmvd
"""

import bz2
from bits_and_bytes import offsets, sizes, header, pad_dict, pad_bufs
from mypath import fpath


i_range = range(3,10)

fname = fpath + '02_HITEMP2024.par.bz2'
sname = 'db/db_subset.txt'

decomp = bz2.BZ2Decompressor()
init = None
with open(fname, 'rb') as fr, open(sname, 'wb') as fw:
    for i in i_range:
        
        # Read compressed block:
        if init is None: 
            fr.seek(offsets[i])
        buf = fr.read(sizes[i])

        # Write alignment block:
        if init is None:
            pad = pad_dict[buf[1]]
            init = decomp.decompress(header + pad_bufs[pad])

        # Write uncompressed data block:
        data = decomp.decompress(buf)
        fw.write(data)

        print(i, offsets[i])

    # Append a byte to trigger decompression of the last block:
    buf = fr.read(1)
    data = decomp.decompress(buf)
    fw.write(data)
    
print('Done!')