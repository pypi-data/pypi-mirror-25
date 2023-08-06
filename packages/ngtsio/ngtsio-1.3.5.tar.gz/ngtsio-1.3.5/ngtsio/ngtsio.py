# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:22:11 2016

@author:
Maximilian N. Guenther
Battcock Centre for Experimental Astrophysics,
Cavendish Laboratory,
JJ Thomson Avenue
Cambridge CB3 0HE
Email: mg719@cam.ac.uk
"""


import numpy as np
import ngtsio_find
import ngtsio_get



###############################################################################
# Define version
###############################################################################
__version__ = '1.3.5'



###############################################################################
# Finder (Main Program)
###############################################################################
def find(RA, DEC, unit='hmsdms', frame='icrs', ngts_version='all', 
         give_obj_id=True, search_radius=0.0014, field_radius=2.):
    print '#RA\tDEC\tfieldname\tngts_version\tobj_id'
    ngtsio_find.find(RA, DEC, unit=unit, frame=frame, ngts_version=ngts_version, 
                     give_obj_id=give_obj_id, search_radius=search_radius, 
                     field_radius=field_radius)
    
    
    
def find_list(fname, usecols=(0,1), unit='hmsdms', frame='icrs', ngts_version='all', 
              give_obj_id=True, search_radius=0.014, field_radius=2.):
    print '#RA\tDEC\tfieldname\tngts_version\tobj_id'
    RAs, DECs = np.genfromtxt(fname, usecols=usecols, delimiter='\t', dtype=None, unpack=True)
    for i in range(len(RAs)):
        ngtsio_find.find(RAs[i], DECs[i])



###############################################################################
# Getter (Main Program)
###############################################################################

def get(fieldname, keys, obj_id=None, obj_row=None, 
        time_index=None, time_date=None, time_hjd=None, time_actionid=None, 
        bls_rank=1, indexing='fits', fitsreader='fitsio', simplify=True, 
        fnames=None, root=None, roots=None, silent=False, ngts_version='TEST18', 
        set_nan=False):

    dic = ngtsio_get.get(fieldname, keys, obj_id=obj_id, obj_row=obj_row, 
        time_index=time_index, time_date=time_date, time_hjd=time_hjd, time_actionid=time_actionid, 
        bls_rank=bls_rank, indexing=indexing, fitsreader=fitsreader, simplify=simplify, 
        fnames=fnames, root=root, roots=roots, silent=silent, ngts_version=ngts_version, 
        set_nan=set_nan)
        
    return dic
 
 