# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 10:05:56 2025

@author: dcmvd
"""
import numpy as np

offsets, pads = np.load('offset_arr.npy')
sizes = offsets[1:] - offsets[:-1]

header = b'BZh91AY&SY'
pad_dict = {65: 0, 130: 1, 5:2, 10:3, 21:4, 43:5, 86:6, 172:7}

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


