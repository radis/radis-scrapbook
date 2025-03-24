# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 21:19:52 2025

@author: dcmvd

This script searches the bzip2 file for the location of block headers
by searching for the block magic 0x314159265359, including its 7 bit-shifted
variants. A separate offsets file is stored for each shift.


"""
import numpy as np
import sys
from mypath import fpath


fname = fpath + '02_HITEMP2024.par.bz2'

chunk_size = 32*1024*1024


#%% bit-shift block headers
blk_hdr_int = 0x314159265359
blk_hdrs = []
for pad in range(8):
    hdr = blk_hdr_int.to_bytes(7)
    print('\n',pad)
    print(hdr.hex())
    print('  '+hdr[1:-1].hex())
    blk_hdrs.append(hdr[1:-1])
    blk_hdr_int <<= 1


#%% Look for block headers:
blk_hdr = blk_hdrs[1]

print('Find block headers...')

offsets = []
with open(fname, 'rb') as fr:
    filesize = fr.seek(0,2)
    
    for pad in range(8): #[:1]:
        blk_hdr = blk_hdrs[pad]
        fr.seek(0,0)    
        buf = b''   
        offsets.append([])
        chunk_id = 0
        i = 0
        
        chunk_offset = 0
        
        while True:
            # Keep finding block headers:
            res = buf[chunk_offset:].find(blk_hdr)
            
            # If none are found, load next buffer:
            if res < 0: 
                # If the current buffer has no more block headers, load a new one:
                buf = fr.read(chunk_size)
                if len(buf):
                    file_offset = chunk_id * chunk_size
                    chunk_offset = 0
                    chunk_id += 1
                    continue
                else:
                    # If the last buffer is empty, we're done
                    break
            else:
                           
                # Otherwise, add the address and increment the counter
                chunk_offset += res
                offsets[-1].append(file_offset + chunk_offset)
                i += 1
                
                # if i > 10: break
                
                # size = offsets[-1] - offsets[-2] if len(offsets) >=2 else 0
                progress = 100*(offsets[-1][-1] / filesize)
                print('{:d}/8 - {:4d} {:12d} {:.2f}% '.format(pad+1, i, offsets[-1][-1], progress))
                
                # Continue search *after* the current header
                chunk_offset += len(blk_hdr)
                
        # If we reach EOF, write the offsets to file:
        offset_arr = np.array(offsets[-1])    
        np.save('offset_arrs/offset_arr_{:d}.npy'.format(pad), offset_arr)    
                
    # If we reach EOF, add the total file size and end the loop:
    # offsets.append(fr.seek(0,2))
    # print('{:4d} {:12d}'.format(i+1, offsets[-1]))

print('Done!')


#%% Merge block offsets:
print('Merging block offset arrays... ')
import numpy as np
from mypath import fpath
fname = fpath + '02_HITEMP2024.par.bz2'

headers = []
bit_shifts = []    

# Find alignment of the end of the last block:
eos_marker = 0x177245385090
with open(fname, 'rb') as fr:
    last_offset = fr.seek(0,2) - 10 #-10 to account for footer_magic + crc
    fr.seek(-10,2)
    buf = fr.read(5)
    # print(buf.hex())
    for pad_end in range(8):
        test_bytes = int(eos_marker << pad_end).to_bytes(7)[1:-1]
        if test_bytes == buf:
            print(pad_end, test_bytes.hex())
            break
        
for pad in range(8):
    
    if True:
        offset_arr = np.load('offset_arrs/offset_arr_{:d}.npy'.format(pad))    
        offset_list = [*offset_arr]
    else:
        offset_list = offsets[pad] #Use the lists from memory
    
    # Add entry for the end of the last block:
    if pad == pad_end:
        offset_list.append(last_offset)
        
    # Accumulate blocks:
    headers += offset_list
    bit_shifts += len(offset_list)*[pad]

# Sort blocks:
merged_array = np.array([headers, bit_shifts])
idx = np.argsort(merged_array[0])
merged_array = merged_array[:, idx]

np.save('offset_arrs/offset_arr.npy', merged_array)
np.save('offset_arr.npy', merged_array)

print('Done!')