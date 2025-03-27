# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:44:45 2025

@author: dcmvd
"""

import bz2
from bits_and_bytes import offsets, header, pad_dict, pad_bufs
from mypath import fpath


i_min, i_max = 3, 9

fname = fpath + '02_HITEMP2024.par.bz2'
sname = 'db/db_subset.txt'


# Read blocks:
with open(fname, 'rb') as fr:
    fr.seek(offsets[i_min])
    buf = fr.read(offsets[i_max + 1] - offsets[i_min])

# Decompress blocks:
decomp = bz2.BZ2Decompressor()
decomp.decompress(header + pad_bufs[pad_dict[buf[1]]])
data = decomp.decompress(buf)
decomp = None

# Write data:       
with open(sname, 'wb') as fw:
    fw.write(data)
    
print('Done!')