# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:44:45 2025

@author: dcmvd
"""

import bz2
from bits_and_bytes import offsets, pad_bufs
from mypath import fpath, my_email, my_password
from hitemp_download import get_bz2
import numpy as np


# total bytesize: 6423107203

offset_dict = {}

wn_arr = np.zeros(len(offsets), dtype=np.float64)

# for i in range(len(offsets) - 1):
for i in range(len(offsets)-1):

    offset = offsets[i]
    size = offsets[i+1] - offsets[i]

    # Read local blocks:
    fname = fpath + '02_HITEMP2024.par.bz2'
    with open(fname, 'rb') as fr:
        fr.seek(offset)
        buf = fr.read(size)
    
    # # Read remote blocks:
    # file_url = r'https://hitran.org/files/HITEMP/bzip2format/02_HITEMP2024.par.bz2'
    # buf = get_bz2(file_url, my_email, my_password, offset=offset, size=size)
    
    
    # Decompress blocks:
    decomp = bz2.BZ2Decompressor()
    decomp.decompress(pad_bufs[buf[1]])
    data = decomp.decompress(buf)
    decomp = None
    buf = None
    
    
    # Find wavenumber
    
    lf_idx = data.find(b'\n')

    # for a complete line, lf_idx would be 160.
    # since the first 3 bytes are molecule and isotope info, we can still find the 
    # wavenumber if lf_idx = 157. Anyhting smaller, we shouldn't try to read this line anymore and advance by 1.
    
    
    if lf_idx >= 157: #current line still has valid wavenumber:
        wn_offs = lf_idx - 157
    else: # discard line and move on to next one:
        wn_offs = lf_idx + 4
    
    wn_str = data[wn_offs:wn_offs + 12].decode()
    wn = float(wn_str)
    offset_dict[wn] = offset
    
    print(f'{i:15d}, {lf_idx:4d}, {wn_str:12s} {lf_idx>=157:1d}')
    wn_arr[i] = wn


# we still have to look up the last wavenumber at the end, but for the moment, let's forget about it    
# the problem is we can't just append the header, cause then bz2 will realize the stream doesnt match the CRC.
# So we should add more fake data, but have to determine the bitshift. We can do this by looking at the footer bytes. 

np.save('wavenumber_arr.npy', wn_arr)
    
    
    
    