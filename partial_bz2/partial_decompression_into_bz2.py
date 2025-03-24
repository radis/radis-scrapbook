# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 08:44:45 2025

@author: dcmvd
"""

import numpy as np
from mypath import fpath
fname = fpath + '02_HITEMP2024.par.bz2'
sname_i = 'db/db_{:05d}.txt.bz2'

offsets, pads = np.load('offset_arr.npy')
sizes = offsets[1:] - offsets[:-1]
N = len(offsets) - 1

def merge_bytes(byte1, byte2, pad):
    mask = 0xff << pad
    return int((byte1 & mask) | (byte2 & (~mask))).to_bytes(1)
    

# def get_block_magic_shifted(pad):
#     # blk_hdr_int = int(0x314159265359 << pad)
#     # return blk_hdr_int.to_bytes(7)[0]
#     return 24 >> (7-pad)


# ## Iterate over pad=0..7 to extract the bytestrings and copy them below
# for pad in range(8):
#     with open('bit_shifts/bit_shift_{:d}.bz2'.format(pad), 'rb') as fr:
#         pad_buf = fr.read()[10:-10] #skip stream header and footer magic+CRC
        
#         # add the shifted bits of the block magic from the data buf:
#         temp_buf = get_block_magic_shifted(pad)
#         temp_buf = merge_bytes(pad_buf[-1], temp_buf, pad)
            
#     print('\t'+str(pad_buf[:-1]+temp_buf)+',')
# sys.exit()


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
eos_marker = 0x177245385090


class StreamCRC:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.strmCRC = 0
    
    def update(self, blkCRC):
        if type(blkCRC) == type(b''):
            blkCRC = int.from_bytes(blkCRC)
        blkCRC &= 0xffffffff
        self.strmCRC = blkCRC ^ ((self.strmCRC<<1) | (self.strmCRC>>31)) 
    
    def result(self):
        return self.strmCRC & 0xffffffff


crc_obj = StreamCRC()
with open(fname, 'rb') as fr:
    for i in [0, 1, 2, N//2-1, N//2, N//2+1, N-3, N-2, N-1]:
        with open(sname_i.format(i), 'wb') as fw:
            print(i, offsets[i], pads[i])
            
            #write alignment block:
            fw.write(stream_header + block_magic + pad_bufs[pads[i]])
            
            # write data block:
            fr.seek(offsets[i])
            buf = fr.read(sizes[i])
            fw.write(buf[:-1])

            # update stream crc:
            crc_obj.reset()
            crc_obj.update(pad_bufs[pads[i]][:4])
            crc_obj.update(int.from_bytes(buf[5:10]) >> pads[i])            
            stream_crc = crc_obj.result()
            
            # write stream footer:
            stream_footer_bin = '{:048b}{:032b}'.format(eos_marker, stream_crc)
            stream_footer_bin += pads[i+1]*'0'
            stream_footer = int(stream_footer_bin, 2).to_bytes(11)
            fw.write(merge_bytes(buf[-1], stream_footer[0], pads[i+1]))
            fw.write(stream_footer[1:])
        
    