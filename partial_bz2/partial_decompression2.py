# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:44:45 2025

@author: dcmvd
"""

import bz2
from bits_and_bytes import offsets, pad_bufs
from mypath import fpath, my_email, my_password
from hitemp_download import get_bz2

# i_min = 0
# i_max = 20

i_min = len(offsets) - 2
i_max = len(offsets) - 2


sname = f'db/db_subset_{i_min:d}_{i_max:d}_.txt'
remote = True


offset = offsets[i_min]
size = offsets[i_max + 1] - offsets[i_min]

if remote: 
    # Read remote blocks:
    file_url = r'https://hitran.org/files/HITEMP/bzip2format/02_HITEMP2024.par.bz2'
    buf = get_bz2(file_url, my_email, my_password, offset=offset, size=size)

else:        
    # Read local blocks:
    fname = fpath + '02_HITEMP2024.par.bz2'
    with open(fname, 'rb') as fr:
        fr.seek(offset)
        buf = fr.read(size)


# Decompress blocks:
decomp = bz2.BZ2Decompressor()
decomp.decompress(pad_bufs[buf[1]])
data = decomp.decompress(buf)
decomp = None
buf = None

# Write data:       
with open(sname, 'wb') as fw:
    fw.write(data)
    
print('Done!')