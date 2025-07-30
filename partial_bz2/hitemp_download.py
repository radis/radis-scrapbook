# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 19:46:07 2025

@author: dcmvd
"""

import requests
import re
from tqdm import tqdm
import io

def get_bz2(file_url, user, pw, offset=None, size=None):
    
    if offset is not None and size is not None:
        range_headers = {'Range': f'bytes={offset}-{offset + size - 1}'}
    else:
        range_headers = {}
    
    session = requests.Session()
    print('Logging in... ', end='')
    # Step 1: Get login page and extract CSRF token
    login_url = 'https://hitran.org/login/'
    resp = session.get(login_url)
    match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', resp.text)
    csrf_token = match.group(1) if match else None
    
    if not csrf_token:
        raise RuntimeError("CSRF token not found")
    
    # Step 2: Log in
    payload = {
        'email': user,
        'password': pw,
        'csrfmiddlewaretoken': csrf_token,
    }
    headers = {'Referer': login_url}
    
    session.post(login_url, data=payload, headers=headers)
    print('Success!')
    
    # Step 3: Download the file
    with session.get(file_url, headers=range_headers, stream=True) as r:
        total = int(r.headers.get('content-length', 0))
        
        buf = io.BytesIO()
        with tqdm(
            desc='Downloading',
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                buf.write(chunk)
                bar.update(len(chunk))
                
    print('\nDownload complete!')
    
    return buf.getvalue()
    

if __name__ == ' __main__':
    
    # file_url = r'https://hitran.org/files/HITEMP/bzip2format/13_HITEMP2024.par.bz2'
    # file_url = r'https://hitran.org/files/HITEMP/bzip2format/10_HITEMP2019.par.bz2'
    file_url = r'https://hitran.org/files/HITEMP/bzip2format/02_HITEMP2024.par.bz2'

    from mypath import my_email, my_password
    buf = get_bz2(file_url, my_email, my_password)
    
    with open(file_url.split('/')[-1], 'wb') as f:
        f.write(buf)
    
    