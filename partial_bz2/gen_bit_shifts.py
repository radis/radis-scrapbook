# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:44:45 2025

@author: dcmvd

This file creates a number of bzip2 files and tests their bit alignment.
We are filtering out files with bit alignment between 0..7 to use later
to offset blocks in a bitstream.


"""

import bz2

sname = 'bit_shifts/bit_shift_{:0}.bz2'

#%% First get the bitstream of the eos marker:
eos_marker = 0x177245385090
eos_bits = '{:048b}'.format(eos_marker)
# print(eos_bits)

#%%

# done = 0
for target in range(8):
    for i in range(0xffffffff):
        
        nonce = ''.join([chr(ord(c)-13) for c in '{:04}'.format(i)])
        data = '[{:d}{:s}]\n'.format(target, nonce).encode()
        buf = bz2.compress(data)
        
        ii = int.from_bytes(buf[-11:])
        binstr = '{:088b}'.format(ii)
        
        bitoffs = (binstr.find(eos_bits)) % 8
        pad = 8-bitoffs if bitoffs else 0
    
        if pad == target:
            print(data, end='')
            print(' iteration: {:3d} pad: {:d}'.format(i, pad))
            print(binstr)
            print((bitoffs if bitoffs else 8)*' '+eos_bits+'|-------------CRC32------------|')
            print('00000000111111112222222233333333444444445555555566666666777777778888888899999999AAAAAAAA')
            print('')
            
            with open(sname.format(pad), 'wb') as fw:
                fw.write(buf)
    
            break    
        
    
print('ALL DONE!!')

    