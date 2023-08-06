# coding: utf-8
# Copyright (c) Henniggroup.
# Distributed under the terms of the MIT License.

from __future__ import division, unicode_literals, print_function

import os
import sys
import operator
import warnings
import yaml
from pymatgen.ext.matproj import MPRester

from monty.serialization import loadfn

__author__ = "Kiran Mathew, Joshua J. Gabriel, Michael Ashton, " \
             "Arunima K. Singh, Joshua T. Paul, Seve G. Monahan, " \
             "Richard G. Hennig"
__date__ = "October 4 2017"
__version__ = "2.0.2"

PACKAGE_PATH = os.path.dirname(__file__)

SETTINGS_FILE = os.path.join(os.path.expanduser('~'),'.mpint_config.yaml')

if not os.path.exists(SETTINGS_FILE):
    user_configs = {key:None for key in ['username','bulk_binary','twod_binary',\
               'sol_binary','ncl_binary','custom_binary',\
               'vdw_kernel','potentials','MAPI_KEY', 'queue_system', 'queue_template']}

    user_configs['queue_system'] = 'slurm'
    user_configs['queue_template'] = PACKAGE_PATH

    with open(os.path.join(os.path.expanduser('~'),'.mpint_config.yaml'),'w') as config_file:
       yaml.dump(user_configs, config_file, default_flow_style=False)


try:
  MPINT_CONFIG = yaml.load(open(SETTINGS_FILE))

  if MPINT_CONFIG.get('potentials',''):
    os.system('export PMG_VASP_PSP_DIR={}'.format(MPINT_CONFIG.get('potentials', '')))

  else:
    warnings.warn('Check your mpint_config.yaml potentials path')
         
  USERNAME = MPINT_CONFIG.get('username', None)
  VASP_STD_BIN = MPINT_CONFIG.get('bulk_binary', None)
  VASP_TWOD_BIN = MPINT_CONFIG.get('twod_binary', None)
  VASP_NCL_BIN = MPINT_CONFIG.get('ncl_binary', None)
  VASP_SOL_BIN = MPINT_CONFIG.get('sol_binary', None)
  VASP_CUSTOM_BIN = MPINT_CONFIG.get('custom_binary', None)
  VDW_KERNEL = MPINT_CONFIG.get('vdw_kernel', None)
  VASP_PSP = MPINT_CONFIG.get('potentials', None)
  MP_API = MPINT_CONFIG.get('MAPI_KEY',None)
  QUEUE_SYSTEM = MPINT_CONFIG.get('queue_system', 'slurm')
  QUEUE_TEMPLATE = MPINT_CONFIG.get('queue_template', PACKAGE_PATH)
  

  try:
     MPR = MPRester(MP_API)
     MPR.get_data('Cu')
     os.system('export MAPI_KEY={}'.format(MP_API))
  except:
     warnings.warn('Check MP_API Key in mpint_config.yaml')
except:
  warnings.warn('Check ~/.mpint_config.yaml file.')

# set environ variables for MAPI_KEY and VASP_PSP_DIR

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
