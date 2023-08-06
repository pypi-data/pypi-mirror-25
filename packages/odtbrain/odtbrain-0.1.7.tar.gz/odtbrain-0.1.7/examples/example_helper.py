#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file contains miscellaneous methods that are used by
example scripts.
"""
from __future__ import print_function


import os
from os.path import dirname, join, exists, isdir
import tarfile

import warnings

datadir = "data"
webloc = "https://github.com/RI-imaging/ODTbrain/raw/master/examples/data"

def dl_file(url, dest, chunk_size=6553):
    """
    Download `url` to `dest`.
    """
    import urllib3
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    with open(dest, 'wb') as out:
        while True:
            data = r.read(chunk_size)
            if data is None or len(data)==0:
                break
            out.write(data)
    r.release_conn()


def get_file(fname):
    """
    Return the full path to a basename. If the file does not exist
    in the current directory or in subdirectory `datadir`, try to 
    download it from the public GitHub repository.
    """
    # download location
    dlloc = join(dirname(__file__), datadir)
    if exists(dlloc):
        if isdir(dlloc):
            pass
        else:
            raise OSError("Must be directory: "+dlloc)
    else:
        os.mkdir(dlloc)
        
    
    # find the file
    foundloc = None
    
    # Search possible file locations
    possloc = [dirname(__file__), dlloc]  

    for pl in possloc:
        if exists(join(pl, fname)):
            foundloc = join(pl, fname)
            break
                
    if foundloc is None:
        # Download file with urllib2.urlopen
        print("Attempting to download file {} from {} to {}.".
              format(fname, webloc, dlloc))
        try:
            dl_file(url=join(webloc, fname),
                    dest=join(dlloc, fname))
        except:
            warnings.warn("Download failed: "+fname)
            raise
        else:
            foundloc = join(dlloc, fname)
    
    if foundloc is None:
        raise OSError("Could not obtain file: "+fname)
    
    return foundloc


def load_tar_lzma_data(afile):
    """
    Load FDTD data from a .tar.lzma file.
    """
    try:
        import lzma
    except ImportError:
        try:
            from backports import lzma
        except ImportError:
            print("Please install lzma with 'pip install backports.lzma'")
    import numpy as np

    # open lzma file
    with open(afile, "rb") as l:
        data = lzma.decompress(l.read())
    # write tar file
    with open(afile[:-5], "wb") as t:
        t.write(data)
    # open tar file
    fields_real = []
    fields_imag = []
    phantom = []
    parms = {}
    
    with tarfile.open(afile[:-5], "r") as t:
        members = t.getmembers()
        members.sort(key=lambda x: x.name)
        
        for m in members:
            n = m.name
            f = t.extractfile(m)
            if n.startswith("fdtd_info"):
                for l in f.readlines():
                    l = l.decode()
                    if l.count("=") == 1:
                        key, val = l.split("=")
                        parms[key.strip()] = float(val.strip())
            elif n.startswith("phantom"):
                phantom.append(np.loadtxt(f))
            elif n.startswith("field"):
                if n.endswith("imag.txt"):
                    fields_imag.append(np.loadtxt(f))
                elif n.endswith("real.txt"):
                    fields_real.append(np.loadtxt(f))

    phantom = np.array(phantom)
    sino = np.array(fields_real)+1j*np.array(fields_imag)
    angles = np.linspace(0, 2*np.pi, sino.shape[0], endpoint=False)
    
    return sino, angles, phantom, parms