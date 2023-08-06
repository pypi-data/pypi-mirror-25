# coding: utf-8
# Copyright (c) Henniggroup.
# Distributed under the terms of the MIT License.

from __future__ import division, unicode_literals, print_function

import os
import sys
import operator
import warnings

#from pymatgen.matproj.rest import MPRester

from monty.serialization import loadfn

__author__ = "Kiran Mathew, Joshua J. Gabriel, Michael Ashton, " \
             "Arunima K. Singh, Joshua T. Paul, Seve G. Monahan, " \
             "Richard G. Hennig"
__date__ = "March 3 2017"
__version__ = "1.7.0"

PACKAGE_PATH = os.path.dirname(__file__)

try:
    MPINT_CONFIG = loadfn(os.path.join(PACKAGE_PATH, 'mpint_config.yaml'))
except:
    MPINT_CONFIG = {}
    warnings.warn('mpint_config.yaml file not configured.')

def set_config():
    """
    set global variables for configuration
    """
    
# set environ variables for MAPI_KEY and VASP_PSP_DIR
    if MPINT_CONFIG['potentials']:
        os.environ['PMG_VASP_PSP_DIR'] = MPINT_CONFIG.get('potentials', '')

    else:
        warnings.warn('Potentials path must be set.. Check your mpint_config.yaml')
        
    if MPINT_CONFIG['MAPI_KEY']:
        os.environ['MAPI_KEY'] = MPINT_CONFIG.get('MAPI_KEY')
    else:
        warnings.warn('MAPI_KEY not set please check your mpint_config.yaml')
    
    USERNAME = MPINT_CONFIG.get('username', None)
    VASP_STD_BIN = MPINT_CONFIG.get('normal_binary', None)
    VASP_TWOD_BIN = MPINT_CONFIG.get('twod_binary', None)
    VDW_KERNEL = MPINT_CONFIG.get('vdw_kernel', None)
    VASP_PSP = MPINT_CONFIG.get('potentials', None)
    MP_API = MPINT_CONFIG.get('MAPI_KEY',None)
 
    QUEUE_SYSTEM = MPINT_CONFIG.get('queue_system', None)
    QUEUE_TEMPLATE = MPINT_CONFIG.get('queue_template', None)

    if not QUEUE_SYSTEM:
        QUEUE_SYSTEM = 'slurm'


    return MPINT_CONFIG, MP_API, VASP_PSP, QUEUE_TEMPLATE,\
         USERNAME, VASP_STD_BIN, VASP_TWOD_BIN, VDW_KERNEL, QUEUE_SYSTEM

set_config()
from pymatgen.matproj.rest import MPRester

try:
   MPR = MPRester(MP_API)
   MPR.get_data('Cu')
except:
   warnings.warn('Error with MP_API Key connection')

def get_struct_from_mp(formula, MAPI_KEY="", all_structs=False):
    """
    fetches the structure corresponding to the given formula
    from the materialsproject database.

    Note: Get the api key from materialsproject website. The one used
    here is nolonger valid.

    Note: for the given formula there are many structures available,
    this function returns the one with the lowest energy above the hull
    unless all_structs is set to True
    """
    if not MAPI_KEY:
        MAPI_KEY = os.environ.get("MAPI_KEY", "")
        if not MAPI_KEY:
            print('API key not provided')
            print(
                'get API KEY from materialsproject and set it to the MAPI_KEY environment variable. aborting ... ')
            sys.exit()
    with MPR as m:
        data = m.get_data(formula)
        structures = []
        x = {}
        print(
            "\nnumber of structures matching the chemical formula {0} = {1}".format(
                formula, len(data)))
        print(
            "The one with the the lowest energy above the hull is returned, unless all_structs is set to True")
        for d in data:
            mpid = str(d['material_id'])
            x[mpid] = d['e_above_hull']
            if all_structs:
                structure = m.get_structure_by_material_id(mpid)
                structures.append(structure)
        if all_structs:
            return structures
        else:
            mineah_key = sorted(x.items(), key=operator.itemgetter(1))[0][0]
            print(
                "The id of the material corresponding to the lowest energy above the hull = {0}".format(
                    mineah_key))
            if mineah_key:
                return m.get_structure_by_material_id(mineah_key)
            else:
                return None
