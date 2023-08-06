# coding: utf-8
# Copyright (c) Henniggroup.
# Distributed under the terms of the MIT License.

from __future__ import division, print_function, unicode_literals, \
    absolute_import


"""
Utility functions
"""

from six.moves import range, zip

import itertools as it
from functools import reduce
import linecache
import sys
import os
import math
import socket
import time
import subprocess as sp
import logging
from collections import OrderedDict
import yaml
from argparse import ArgumentParser

from glob import glob
import numpy as np
import pandas as pd

from monty.json import MontyEncoder, MontyDecoder
from monty.serialization import loadfn, dumpfn

from pymatgen.core.sites import PeriodicSite
from pymatgen import Structure, Lattice, Element
from pymatgen.core.surface import Slab, SlabGenerator
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.vasp.inputs import Poscar
from pymatgen.core.composition import Composition
from pymatgen.core.operations import SymmOp
from pymatgen.io.vasp.inputs import Incar, Kpoints
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.symmetry.bandstructure import HighSymmKpath

from custodian.custodian import Custodian
from custodian.vasp.handlers import VaspErrorHandler

from fireworks.user_objects.queue_adapters.common_adapter import CommonAdapter

from ase.lattice.surface import surface

from mpinterfaces.default_logger import get_default_logger
from mpinterfaces import set_config, PACKAGE_PATH

MPINT_CONFIG, MP_API, VASP_PSP, QUEUE_TEMPLATE, USERNAME,\
 VASP_STD_BIN, VASP_TWOD_BIN, VDW_KERNEL, QUEUE_SYSTEM = set_config()
#from mpinterfaces import VASP_STD_BIN, QUEUE_SYSTEM, QUEUE_TEMPLATE, VASP_PSP,\
# PACKAGE_PATH

__author__ = "Kiran Mathew, Joshua J. Gabriel"
__copyright__ = "Copyright 2017, Henniggroup"
__maintainer__ = "Joshua J. Gabriel"
__email__ = "joshgabriel92@gmail.com"
__status__ = "Production"
__date__ = "March 3, 2017"

logger = get_default_logger(__name__)


def get_ase_slab(pmg_struct, hkl=(1, 1, 1), min_thick=10, min_vac=10):
    """
    takes in the intial structure as pymatgen Structure object
    uses ase to generate the slab
    returns pymatgen Slab object

    Args:
        pmg_struct: pymatgen structure object
        hkl: hkl index of surface of slab to be created
        min_thick: minimum thickness of slab in Angstroms
        min_vac: minimum vacuum spacing
    """
    ase_atoms = AseAtomsAdaptor().get_atoms(pmg_struct)
    pmg_slab_gen = SlabGenerator(pmg_struct, hkl, min_thick, min_vac)
    h = pmg_slab_gen._proj_height
    nlayers = int(math.ceil(pmg_slab_gen.min_slab_size / h))
    ase_slab = surface(ase_atoms, hkl, nlayers)
    ase_slab.center(vacuum=min_vac / 2, axis=2)
    pmg_slab_structure = AseAtomsAdaptor().get_structure(ase_slab)
    return Slab(lattice=pmg_slab_structure.lattice,
                species=pmg_slab_structure.species_and_occu,
                coords=pmg_slab_structure.frac_coords,
                site_properties=pmg_slab_structure.site_properties,
                miller_index=hkl, oriented_unit_cell=pmg_slab_structure,
                shift=0., scale_factor=None, energy=None)


def slab_from_file(hkl, filename):
    """
    reads in structure from the file and returns slab object.
    useful for reading in 2d/substrate structures from file.
    Args:
         hkl: miller index of the slab in the input file.
         filename: structure file in any format
                   supported by pymatgen
    Returns:
         Slab object
    """
    slab_input = Structure.from_file(filename)
    return Slab(slab_input.lattice,
                slab_input.species_and_occu,
                slab_input.frac_coords,
                hkl,
                Structure.from_sites(slab_input, to_unit_cell=True),
                shift=0,
                scale_factor=np.eye(3, dtype=np.int),
                site_properties=slab_input.site_properties)


def get_hse_kpoints_file(struct_for_path, ibzkpth, density=20, twod=False, test_print=False):
    """
    gets a HSE kpoints bands structure file by piecing together
    the HighSymmKpath with the IBZKPT

    Args:
        struct_for_path: Structure from which linemode k-points will be generated.
        ibzkpth: path to IBZKPT file

    Returns:
        the Kpoints file object in the form of a string
              ready for execution by MPInterfaces
              calibrate objects
    """
    # Read IBZKPT from prep step
    ibz_lines = open(ibzkpth).readlines()
    n_ibz_kpts = int(ibz_lines[1].split()[0])

    # Read linemode KPOINTs from the dict (makes sure it is Kpoints
    # file with general density input, 20 per atom by default for the optimized settings
    kpath = HighSymmKpath(struct_for_path)
    Kpoints.automatic_linemode(density, kpath).write_file('KPOINTS_linemode')
    if twod:
       remove_z_kpoints_linemode()
    ## Now the following part is what needs to undergo the major general test for
    ## correctness. Do they remove z kpoints for the IBZKPT? in 2D materials as well?
    linemode_lines = open('KPOINTS_linemode').readlines()

    # put them together
    abs_path = []
    i = 4
    while i < len(linemode_lines):
             start_kpt = linemode_lines[i].split()
             end_kpt = linemode_lines[i+1].split()
             increments = [
                 (float(end_kpt[0]) - float(start_kpt[0])) / density,
                 (float(end_kpt[1]) - float(start_kpt[1])) / density,
                 (float(end_kpt[2]) - float(start_kpt[2])) / density
             ]
             abs_path.append(start_kpt[:3] + ['0', start_kpt[4]])
             for n in range(1, 20):
                 abs_path.append(
                     [str(float(start_kpt[0]) + increments[0] * n),
                      str(float(start_kpt[1]) + increments[1] * n),
                      str(float(start_kpt[2]) + increments[2] * n), '0']
                     )
             abs_path.append(end_kpt[:3] + ['0', end_kpt[4]])
             i += 3

    n_linemode_kpts = len(abs_path)

    # write out the kpoints file and return the object

    Kpoints_hse_file = '\n'.join(
        ['Automatically generated mesh',
         '{}'.format(n_ibz_kpts + n_linemode_kpts),
         'Reciprocal Lattice',
         '{}'.format(str(''.join([line for line in ibz_lines[3:]])))]) + \
                       '{}'.format(str('\n'.join(
                           [' '.join(point) for point in abs_path])))
    if test_print:
       print (Kpoints_hse_file)
    else:
       # explore a way if the above can be dictified into a pymatgen Kpoints object
       # for now a string gets returned which is written out by instrument
       return Kpoints_hse_file
        
    pass

def get_hse_prep_incar(incar_dict):
    """
    general hse prep incar file that is used 
    to just generate a mellowed down version
    of the IBZKPT
    """
    INCAR_PREP = {'NSW': 0,
                  'NELM': 1,
                  'LWAVE': False,
                  'LCHARG': False,
                  'LAECHG': False}
    incar_dict.update(INCAR_PREP)
    return incar_dict

def get_hse_incar(incar_dict):
    """
    a general hse incar template based on what
    the materialsweb database was built on.
    
    NOTE: Use this with care for bulk materials 
    especially if a CHGCAR or WAVECAR with a different
    ENCUT is also being used. 

    Args:
        incar_dict (dict)

    Returns:
        dict: incar dict
    """
    HSE_INCAR_DICT = {'LHFCALC': True, 'HFSCREEN': 0.2, 'AEXX': 0.25,
                      'ALGO': 'D', 'TIME': 0.4, 'NSW': 0, 'NELM': 75,
                      'LVTOT': True, 'LVHAR': True, 'LORBIT': 11,
                      'LWAVE': False, 'NPAR': 8, 'PREC': 'Accurate',
                      'EDIFF': 1e-4, 'ENCUT': 450, 'ICHARG': 2, 'ISMEAR': 1,
                      'SIGMA': 0.1, 'IBRION': 2, 'ISIF': 3, 'ISPIN': 2}
    incar_dict.update(HSE_INCAR_DICT)
    return incar_dict
    

def get_magmom_string(structure):
    """
    Based on a POSCAR, returns the string required for the MAGMOM
    setting in the INCAR. Initializes transition metals with 6.0
    bohr magneton and all others with 0.5.
    TEST: integration of mat2d function with mpinterfaces
    calibrate.py
    Consider moving to mpinterfaces.utils

    Args:
        structure (Structure): Pymatgen Structure object

    Returns:
        string with INCAR setting for MAGMOM according to mat2d
        database calculations
    """
    magmoms, considered = [], []
    for s in structure.sites:
        if s.specie not in considered:
            if s.specie.is_transition_metal:
                magmoms.append('{}*6.0'.format(structure.composition[s.specie]))
            else:
                magmoms.append('{}*0.5'.format(structure.composition[s.specie]))
            considered.append(s.specie)
    return ' '.join(magmoms)


def get_magmom_mae(poscar, mag_init):
    """
    mae
    """
    mae_magmom = []

    sites_dict = poscar.as_dict()['structure']['sites']

    # initialize a magnetic moment on the transition metal
    # in vector form on the x-direction
    for n, s in enumerate(sites_dict):

        if Element(s['label']).is_transition_metal:
            mae_magmom.append([0.0, 0.0, mag_init])
        else:
            mae_magmom.append([0.0, 0.0, 0.0])

    return sum(mae_magmom, [])


def get_magmom_afm(poscar, database=None):
    """
    returns the magmom string which is an N length list
    """

    afm_magmom = []
    orig_structure_name = poscar.comment

    if len(poscar.structure) % 2 != 0:

        if database == 'twod':
            # no need for more vacuum spacing
            poscar.structure.make_supercell([2, 2, 1])
        else:
            # for bulk structure
            poscar.structure.make_supercell([2, 2, 2])

    sites_dict = poscar.as_dict()['structure']['sites']

    for n, s in enumerate(sites_dict):

        if Element(s['label']).is_transition_metal:
            if n % 2 == 0:
                afm_magmom.append(6.0)
            else:
                afm_magmom.append(-6.0)

        else:
            if n % 2 == 0:
                afm_magmom.append(0.5)
            else:
                afm_magmom.append(-0.5)

    return afm_magmom, Poscar(structure=poscar.structure,
                              comment=orig_structure_name)

    
def get_magmom_hunds(poscar):
    """
    returns the Hund's rule following 
    initialization for magnetism
    """
    magmom_string = []
    quantum_num = {'s':0,'p':1,'d':2,'f':'3'}
    for el in poscar.structure.species:
       econfig = {key: None for key in \
         ['1s','2s','2p','3s','3p','3d','4s','4p','4d','4f',\
          '5s','5p','5d','5f','6s','6p','6d']}
       elec_struct_el = Element(el).full_electronic_structure
       for q in elec_struct_el:
          econfig[str(q[0])+q[1]] = q[2]
       for k in list(econfig.keys()):
          if econfig[k]==None:
             del econfig[k]
       #for k in list(econfig.keys()):
       mag_num = 0
       for c,n in econfig.items():
          if n%2!=0:
             print (c,n)
             if 's' in c:
                mag_num += 1
             elif 'p' in c:
                if n <= 3:
                   mag_num += n
                else:
                   mag_num += 6-n
             elif 'd' in c:
                if n <= 5:
                   mag_num += n
                else:
                   mag_num += 10-n
             elif 'f' in c:
                if n <= 7:
                   mag_num += n
                else:
                   mag_num += 14-n
       magmom_string.append(mag_num)

    return magmom_string

def get_magmom_custom(poscar):
    """
    set the magmom initialization in a 
    custom fashion 
    """
    pass 


def get_mueller_kpoints(kppra):
    """
    returns k-points grid for a structure based on algo
    found in ...
    NOTE: requirements, PRECALC_temp and getKPoints must be in 
    the current working directory
    """
    prec_file = Incar.from_file('PRECALC_temp')
    prec_file['KPPRA']=kppra 
    prec_file.write_file('PRECALC')
    os.system('./getKPoints')
    return Kpoints.from_file('KPOINTS')

def load_config(update_config=None):
    """
    helper function which will load all the mpinterfaces variables
    """
    pass 

def get_run_cmmnd(nnodes=1, ntasks=16, walltime='24:00:00', job_bin=None,
                  job_name=None, mem=None, update_template=None, partition='hpg1-compute'):
    """
    returns the fireworks CommonAdapter based on the queue
    system specified by mpint_config.yaml and the submit
    file template also specified in mpint_config.yaml
    NOTE: for the job_bin, please specify the mpi command as well:
          Eg: mpiexec /path/to/binary 
    """
    d = {}
    job_cmd = None
    qtemp = yaml.load(open(QUEUE_TEMPLATE))
    if update_template:
       qtemp.update(yaml.load(open(update_template)))

    qtemp.update({'nnodes': nnodes, 'ntasks':ntasks, 'walltime': walltime, \
                  'rocket_launch': job_bin, 'job_name':job_name,'mem':mem,\
                  'hpg-partition': partition})

    # user puts in a cell with number of atoms
    # translates to a number of tasks = 2, 4, 8, 16, 32, 64
    # decide which compute node partition is more available
    # if hpg1: 4 sockets x 16 tasks_per_socket = 64 max tasks per node
    # elif hpg2: 2 sockets x 16 tasks_per_socket = 32 max tasks per node

    # say ntasks = 32, hpg2 - 2 sockets
    qtemp['ntasks_per_node'] = int(qtemp['ntasks']/qtemp['nnodes'])
    # say nnodes = 1, gives ntasks_per_node = 32, divide into 16 per socket
    # say nnodes = 2, gives ntasks_per_node = 16, divide into 8 per socket
    # say nnodes = 4, gives ntasks_per_node = 8, divide into 4 per socket 
   
    if qtemp['partition'] == 'hpg1-compute':
       qtemp['ntasks_per_socket'] = int(qtemp['ntasks_per_node']/4)

    elif qtemp['partition'] == 'hpg2-compute':
       qtemp['ntasks_per_socket'] = int(qtemp['ntasks_per_node']/2)

    # SLURM queue
    if QUEUE_SYSTEM == 'slurm':
        if job_bin is None:
            job_bin = VASP_STD_BIN
        else:
            job_bin = job_bin
        d = {'type': 'SLURM',
             'params': qtemp}
    # PBS queue
    elif QUEUE_SYSTEM == 'PBS':
        if job_bin is None:
            job_bin = VASP_STD_BIN
        else:
            job_bin = job_bin
        d = {'type': 'PBS',
             'params': qtemp}
    else:
        job_cmd = ['ls', '-lt']
    if d:
        return (CommonAdapter(d['type'], **d['params']), job_cmd)
    else:
        return (None, job_cmd)


def get_job_state(job):
    """
    Args:
        job: job

    Returns:
           the job state and the job output file name
    """
    # hostname = socket.gethostname()

    # hipergator
    if QUEUE_SYSTEM == 'slurm':# in hostname:
        try:
            output = sp.check_output(['squeue', '-i', job.job_id])
            state = output.rstrip('\n').split('\n')[-1].split()[-2]
        except:
            logger.info('Job {} not in the que'.format(job.job_id))
            state = "00"
        err_file = glob(job.job_dir+os.sep+'*.error')[0]
        out_file = err_file.split('.')[0] + '.out'

    #"FW_job.out"

    # stampede, slurm
    # else: #'stampede' in hostname:
    #    try:
    #        output = sp.check_output(['squeue', '--job', job.job_id])
    #        state = output.rstrip('\n').split('\n')[-1].split()[-4]
    #    except:
    #        logger.info('Job {} not in the que.'.format(job.job_id))
    #        logger.info(
    #            'This could mean either the batchsystem crashed(highly unlikely) or the job completed a long time ago')
    #        state = "00"
    #    ofname = "vasp_job-" + str(job.job_id) + ".out"

    # no batch system
    else:
        state = 'XX'
    return state, out_file


def update_checkpoint(job_ids=None, jfile=None, **kwargs):
    """
    rerun the jobs with job ids in the job_ids list. The jobs are
    read from the json checkpoint file, jfile.
    If no job_ids are given then the checkpoint file will
    be updated with corresponding final energy

    Args:
        job_ids: list of job ids to update or q resolve
        jfile: check point file
    """
    cal_log = loadfn(jfile, cls=MontyDecoder)
    cal_log_new = []
    all_jobs = []
    run_jobs = []
    handlers = []
    final_energy = None
    incar = None
    kpoints = None
    qadapter = None
    # if updating the specs of the job
    for k, v in kwargs.items():
        if k == 'incar':
            incar = v
        if k == 'kpoints':
            kpoints = v
        if k == 'que':
            qadapter = v
    for j in cal_log:
        job = j["job"]
        job.job_id = j['job_id']
        all_jobs.append(job)
        if job_ids and (j['job_id'] in job_ids or job.job_dir in job_ids):
            logger.info('setting job {0} in {1} to rerun'.format(j['job_id'],
                                                                 job.job_dir))
            contcar_file = job.job_dir + os.sep + 'CONTCAR'
            poscar_file = job.job_dir + os.sep + 'POSCAR'
            if os.path.isfile(contcar_file) and len(
                    open(contcar_file).readlines()) != 0:
                logger.info('setting poscar file from {}'
                            .format(contcar_file))
                job.vis.poscar = Poscar.from_file(contcar_file)
            else:
                logger.info('setting poscar file from {}'
                            .format(poscar_file))
                job.vis.poscar = Poscar.from_file(poscar_file)
            if incar:
                logger.info('incar overridden')
                job.vis.incar = incar
            if kpoints:
                logger.info('kpoints overridden')
                job.vis.kpoints = kpoints
            if qadapter:
                logger.info('qadapter overridden')
                job.vis.qadapter = qadapter
            run_jobs.append(job)
    if run_jobs:
        c = Custodian(handlers, run_jobs, max_errors=5)
        c.run()
    for j in all_jobs:
        final_energy = j.get_final_energy()
        #latest_structure = j.get_latest_structure()
        cal_log_new.append({"job": j.as_dict(),
                            'job_id': j.job_id,
                            "corrections": [],
                            'final_energy': final_energy})
                            #'latest_structure': latest_structure})
    dumpfn(cal_log_new, jfile, cls=MontyEncoder, indent=4)


def jobs_from_file(filename='calibrate.json'):
    """
    read in json file of format caibrate.json(the default logfile
    created when jobs are run through calibrate) and return the
    list of job objects.

    Args:
        filename: checkpoint file name

    Returns:
           list of all jobs
    """
    caljobs = loadfn(filename, cls=MontyDecoder)
    all_jobs = []
    for j in caljobs:
        job = j["job"]
        job.job_id = j['job_id']
        job.final_energy = j['final_energy']
        all_jobs.append(job)
    return all_jobs


def continue_job_inputs(chkpt_files=None, old_job_dir=None, user_filters=None,\
                     rerun_nonconverged_also=False):
   """
   utility function for any workflow that can be used to decide which
   materials pass to the next stage of a workflow
   """
   if chkpt_files:
      # Fuel source from checkpoint files
      rerun_paths = []
      chkpts = sum( [ jobs_from_file(j) for j in \
                    [chks for chks in chkpt_files]], []  )

      all_converged = [ (j.parent_job_dir+os.sep+j.job_dir,\
        j.job_dir.split('/')[-1].split('_')[0],\
        j.job_dir.split('/')[-1].split('_')[-1])\
        for j in chkpts if j.final_energy ]

      restarts = [ (j.parent_job_dir+os.sep+j.job_dir,\
        j.job_dir.split('/')[-1].split('_')[0],\
        j.job_dir.split('/')[-1].split('_')[-1])\
        for j in chkpts if not j.final_energy ]

      if user_filters:
           # filter based on compound and structure name tags
           # can be on more involved factors like % of jobs done in the step
           filtered_run = yaml.load(open(user_filters))
           for (job_path, compound, structure) in all_converged:
              for f in filtered_run.keys():
                 for s in filtered_run[f]:
                    if f == compound and s == structure:
                       rerun_paths.append(job_path)
      else:
          rerun_paths = [p[0] for p in all_converged]

   elif old_job_dir:
       # Fuel source from list of directories
       rerun_paths = old_job_dirs

   if rerun_nonconverged_also:
       return rerun_paths, restarts
   else:
       return rerun_paths

def check_job_with_custodian(handlers,logfile,job=None,jdir=None):
    """
    function which checks a given checkpoint job 
    or a job directory for errors and performs 
    either just in time correction (writes STOPCAR to a job
    that is running with errors and re-submits to the queue
    with a corrected input set. 
    or correction 
    """
    corrected={'ErrorDir':[],'Error':[],'Correction':[]}
    if job:
      j = job
      with open(j.parent_job_dir+os.sep+j.job_dir+os.sep+j.output_file) as w:
        j_num = w.read()
      w.close()
      out_file = '-'.join([j.vis.qadapter['job_name'],j_num]) + '.out'
      err_file = '-'.join([j.vis.qadapter['job_name'],j_num]) + '.err'
      output_path = j.parent_job_dir+os.sep+j.job_dir
      if os.path.exists(output_path+os.sep+out_file):
        for h in handlers:
           h.output_filename = out_file
           os.chdir(j.job_dir)
           try:
               if h.check():
                   logfile.info('Making correction to {0} \n \
                               and detected errors are {1} \n \
                               Custodian correction is {2}'.\
                           format(output_path,h.errors, h.correct()))
                   #logfile.info('Detected errors are: {}'.format(h.errors))
                   #logfile.info('Correction from Custodian is {}'.format(h.correct()))
                   corrected['ErrorDir'].append(output_path)
                   corrected['Error'].append(h.errors)
                   corrected['Correction'].append(h.correct())
               else:
                   logfile.info('Custodian correction unavailable for {}'.format(output_path))
                   corrected['ErrorDir'].append(output_path)
                   corrected['Error'].append('CU')
                   corrected['Correction'].append('CU')
           except:
                 logfile.info('Custodian encountered an error')
                 corrected['ErrorDir'].append(output_path)
                 corrected['Error'].append('XX')
                 corrected['Correction'].append('XX')

           os.chdir(j.parent_job_dir)
      else:
        logfile.warn('File does not exist: {}'.format(output_path+os.sep+out_file))
      
      if corrected:
          return corrected
      else:
          return None

    elif jdir:
      pass

    else:
      logger.warn('No job or job directory specified for custodian to check...')
      return None

def launch_daemon(steps, interval, handlers=None, ld_logger=None):
    """
    run all the 'steps' in daemon mode
    checks job status every 'interval' seconds
    also runs all the error handlers
    """
    if ld_logger:
        global logger
        logger = ld_logger
    chkpt_files_prev = None
    for step in steps:
        chkpt_files = step(checkpoint_files=chkpt_files_prev)
        #print (chkpt_files, type(chkpt_files))
        chkpt_files_prev = chkpt_files
        if not chkpt_files:
            return None
        while True:
            done = []
            reruns = []
            for cf in chkpt_files:
                time.sleep(3)
                print (reruns)
                update_checkpoint(job_ids=reruns, jfile=cf)
                all_jobs = jobs_from_file(cf)
                for j in all_jobs:
                    state, ofname = get_job_state(j)
                    logger.info('Job {0} in {1} state is {2}'.format(j.job_id,j.job_dir,state))
                    # decide on actions first based on job state 
                    # 1. if finished and final energy exists, done to True
                    # 2. If waiting in q report waiting in q and done to false
                    # 3. If running in q : done to false and check errors 
                    # (just-in time corrections.. could be write a STOPCAR 
                    # and restart with corrected input set)
                    # 4. If finished in q: done to false and check errors and 
                    # create rerun list with corrected parameters to be re-launched 
                    if j.final_energy:
                        logger.info('Job {} done with converged energy'.format(j.job_id))
                        done = done + [True]
                    elif state in ['Q','PD']:
                        logger.info('Job {} waiting in q'.format(j.job_id))
                        done = done + [False]
                    elif state in ['R','C', 'CF', 'F', '00']:
                        # Handling cases can be: 
                        # 1. Finished and failed: Custodian correct and add to rerun list 
                        # 2. running normally and no errors 
                        # 3. running, but with errors
                        done = done + [False]
                        if state == 'R':
                             logger.info('Job {} running'.format(j.job_id))
                        else:
                             logger.error(
                              'Job {0} in {1} cancelled or failed. State = {2}'.
                              format(j.job_id, j.job_dir, state))
                        if handlers:
                            logger.info('Investigating with Custodian... ')
                            handled_job = check_job_with_custodian(job=j,handlers=handlers)
                            if handled_job and state=='R':
                                reruns.append(j.job_dir)
                                os.chdir(j.job_dir)
                                with open('STOPCAR','w') as f:
                                    f.write()
                                f.close()
                                os.chdir(j.parent_job_dir)
                            elif handled_job and state in ['C','CF','00','F']:
                                reruns.append(j.job_dir)                                        
                    else:
                        logger.info(
                            'Job {0} pending. State = {1}'.format(j.job_id,
                                                                  state))
                        done = done + [False]
            if all(done):
                logger.info(
                    'all jobs in {} done. Proceeding to the next one'.format(
                        step.__name__))
                time.sleep(5)
                break
            logger.info(
                'all jobs in {0} NOT done. Next update in {1} seconds'.format(
                    step.__name__, interval))
            time.sleep(interval)


def get_convergence_data(jfile, params=('ENCUT', 'KPOINTS')):
    """
    returns data dict in the following format
    {'Al':
          {'ENCUT': [ [500,1.232], [600,0.8798] ],
            'KPOINTS':[ [], [] ]
          },
     'W': ...
    }

    Note: processes only INCAR parmaters and KPOINTS
    """
    cutoff_jobs = jobs_from_file(jfile)
    data = {}
    for j in cutoff_jobs:
        jdir = os.path.join(j.parent_job_dir, j.job_dir)
        poscar_file = os.path.join(jdir, 'POSCAR')
        struct_m = Structure.from_file(poscar_file)
        species = ''.join([tos.symbol for tos in struct_m.types_of_specie])
        if data.get(species):
            for p in params:
                if j.vis.incar.get(p):
                    data[species][p].append([j.vis.incar[p],
                                             j.final_energy / len(struct_m)])
                elif p == 'KPOINTS':
                    data[species]['KPOINTS'].append([j.vis.kpoints.kpts,
                                                     j.final_energy / len(
                                                         struct_m)])
                else:
                    logger.warn(
                        'dont know how to parse the parameter {}'.format(p))
        else:
            data[species] = {}
            for p in params:
                data[species][p] = []
                data[species][p] = []
    return data


def get_opt_params(data, species, param='ENCUT', ev_per_atom=0.001):
    """
    return optimum parameter
    default: 1 meV/atom
    """
    sorted_list = sorted(data[species][param], key=lambda x: x[1])
    sorted_array = np.array(sorted_list)
    consecutive_diff = np.abs(
        sorted_array[:-1, 1] - sorted_array[1:, 1] - ev_per_atom)
    min_index = np.argmin(consecutive_diff)
    return sorted_list[min_index][0]


# PLEASE DONT CHANGE THINGS WITHOUT UPDATING SCRIPTS/MODULES THAT DEPEND
# ON IT
# get_convergence_data and get_opt_params moved to *_custom
def get_convergence_data_custom(jfile, params=('ENCUT', 'KPOINTS')):
    """
    returns data dict in the following format
    {'Al':
          {'ENCUT': [ [500,1.232], [600,0.8798] ],
            'KPOINTS':[ [], [] ]
          },
     'W': ...
    }

    Note: processes only INCAR parmaters and KPOINTS
    Sufficient tagging of the data assumed from species,Poscar
    comment line and potcar functional
    """
    cutoff_jobs = jobs_from_file(jfile)
    data = {}
    for j in cutoff_jobs:
        jdir = os.path.join(j.parent_job_dir, j.job_dir)
        poscar_file = os.path.join(jdir, 'POSCAR')
        struct_m = Structure.from_file(poscar_file)

        species = ''.join([tos.symbol for tos in struct_m.types_of_specie])
        tag = '_'.join([species, Poscar.from_file(poscar_file).comment,
                        j.vis.potcar.functional])
        if data.get(tag):
            for p in params:
                if j.vis.incar.get(p):
                    data[tag][p].append([j.vis.incar[p],
                                         j.final_energy / len(struct_m),
                                         j.vis.potcar, j.vis.poscar])
                    #                print(j.vis.potcar.functional,j.vis.poscar)
                elif p == 'KPOINTS':
                    data[tag]['KPOINTS'].append([j.vis.kpoints.kpts,
                                                 j.final_energy / len(
                                                     struct_m), j.vis.potcar,
                                                 j.vis.poscar])
                else:
                    logger.warn(
                        'dont know how to parse the parameter {}'.format(p))
        else:
            data[tag] = {}
            for p in params:
                data[tag][p] = []
                data[tag][p] = []
    return data


def get_opt_params_custom(data, tag, param='ENCUT', ev_per_atom=1.0):
    """
    Args:
        data:  dictionary of convergence data
        tag:   key to dictionary of convergence dara
        param: parameter to be optimized
        ev_per_atom: minimizing criterion in eV per unit

    Returns
        [list] optimum parameter set consisting of tag, potcar object,
        poscar object, list of convergence data energies sorted according to
        param

    default criterion: 1 meV/atom
    """
    sorted_list = sorted(data[tag][param], key=lambda x: x[0])
    # sorted array data
    t = np.array(sorted_list)[:, 1]
    # print(sorted_array[:-1,1], sorted_array[1:,1], ev_per_atom)
    consecutive_diff = [float(j) - float(i) - ev_per_atom for i, j in
                        zip(t[:-1], t[1:])]
    # print("Consecutive_diff",consecutive_diff)
    min_index = np.argmin(consecutive_diff)
    # return the tag,potcar object, poscar object, incar setting and
    # convergence data for plotting that is optimum
    return [tag, data[tag][param][min_index][2],
            data[tag][param][min_index][3], sorted_list[min_index][0], t]


def partition_jobs(turn_knobs, max_jobs):
    """
    divide turn_knobs into smaller turn_knobs so that each one of
    them has smaller max_jobs jobs
    """
    params_len = [len(v) for k, v in turn_knobs.items()]
    n_total_jobs = reduce(lambda x, y: x * y, params_len)
    partition_size = int(n_total_jobs / max_jobs)
    max_index = np.argmax(params_len)
    max_len = max(params_len)
    max_key = list(turn_knobs.items())[max_index][0]
    partition = range(0, max_len, max(1, int(max_len / partition_size)))
    partition_1 = partition[1:] + [max_len]
    logger.info(
        '{0} list of length {1} will be partitioned into {2} chunks'.format(
            max_key, max_len, len(partition)))
    turn_knobs_list = []
    name_list = []
    for i, j in zip(partition, partition_1):
        ordered_list = []
        for k, v in turn_knobs.items():
            if k == max_key:
                tk_item = (k, v[i:j])
            else:
                tk_item = (k, v)
            ordered_list.append(tk_item)
        turn_knobs_list.append(OrderedDict(ordered_list))
        name_list.append('_'.join([str(i), str(j)]))
    return turn_knobs_list, name_list


def get_logger(log_file_name):
    """
    writes out logging file.
    Very useful project logging, recommended for use
    to monitor the start and completion of steps in the workflow
    Arg:
        log_file_name: name of the log file, log_file_name.log
    """
    loggr = logging.getLogger(log_file_name)
    loggr.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    fh = logging.FileHandler(log_file_name + '.log', mode='a')
    fh.setFormatter(formatter)
    loggr.addHandler(fh)
    return loggr


def set_sd_flags(poscar_input=None, n_layers=2, top=True, bottom=True,
                 poscar_output='POSCAR2'):
    """
    set the relaxation flags for top and bottom layers of interface.
    The upper and lower bounds of the z coordinate are determined
    based on the slab.
    Args:
         poscar_input: input poscar file name
         n_layers: number of layers to be relaxed
         top: whether n_layers from top are be relaxed
         bottom: whether n_layers from bottom are be relaxed
         poscar_output: output poscar file name
    Returns:
         None
         writes the modified poscar file
    """
    poscar1 = Poscar.from_file(poscar_input)
    sd_flags = np.zeros_like(poscar1.structure.frac_coords)
    z_coords = poscar1.structure.frac_coords[:, 2]
    z_lower_bound, z_upper_bound = None, None
    if bottom:
        z_lower_bound = np.unique(z_coords)[n_layers - 1]
        sd_flags[np.where(z_coords <= z_lower_bound)] = np.ones((1, 3))
    if top:
        z_upper_bound = np.unique(z_coords)[-n_layers]
        sd_flags[np.where(z_coords >= z_upper_bound)] = np.ones((1, 3))
    poscar2 = Poscar(poscar1.structure, selective_dynamics=sd_flags.tolist())
    poscar2.write_file(filename=poscar_output)


def print_exception():
    """
    Error exception catching function for debugging
    can be a very useful tool for a developer
    move to utils and activate when debug mode is on
    """
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno,
                                                       line.strip(), exc_obj))


def is_converged(directory):
    """
    Check if a relaxation has converged.

    Args:
        directory (str): path to directory to check.

    Returns:
        boolean. Whether or not the job is converged.
    """

    try:
        return Vasprun('{}/vasprun.xml'.format(directory)).converged
    except:
        return False


def get_spacing(structure):
    """
    Returns the interlayer spacing for a 2D material or slab.

    Args:
        structure (Structure): Structure to check spacing for.
        cut (float): a fractional z-coordinate that must be within
            the vacuum region.

    Returns:
        float. Spacing in Angstroms.
    """

    structure = align_axis(structure)
    structure = center_slab(structure)
    max_height = max([s.coords[2] for s in structure.sites])
    min_height = min([s.coords[2] for s in structure.sites])
    return structure.lattice.c - (max_height - min_height)


def center_slab(structure):
    """
    Centers the atoms in a slab structure around 0.5
    fractional height.

    Args:
        structure (Structure): Structure to center
    Returns:
        Centered Structure object.
    """

    center = np.average([s._fcoords[2] for s in structure.sites])
    translation = (0, 0, 0.5 - center)
    structure.translate_sites(range(len(structure.sites)), translation)
    return structure


def add_vacuum(structure, vacuum):
    """
    Adds padding to a slab or 2D material.

    Args:
        structure (Structure): Structure to add vacuum to
        vacuum (float): Vacuum thickness to add in Angstroms
    Returns:
        Structure object with vacuum added.
    """
    structure = align_axis(structure)
    coords = [s.coords for s in structure.sites]
    species = [s.specie for s in structure.sites]
    lattice = structure.lattice.matrix
    lattice[2][2] += vacuum
    structure = Structure(lattice, species, coords, coords_are_cartesian=True)
    return center_slab(structure)


def ensure_vacuum(structure, vacuum):
    """
    Adds padding to a slab or 2D material until the desired amount
    of vacuum is reached.

    Args:
        structure (Structure): Structure to add vacuum to
        vacuum (float): Final desired vacuum thickness in Angstroms
    Returns:
        Structure object with vacuum added.
    """

    structure = align_axis(structure)
    spacing = get_spacing(structure)
    structure = add_vacuum(structure, vacuum - spacing)
    return center_slab(structure)


def get_rotation_matrix(axis, theta):
    """
    Find the rotation matrix associated with counterclockwise rotation
    about the given axis by theta radians.
    Credit: http://stackoverflow.com/users/190597/unutbu

    Args:
        axis (list): rotation axis of the form [x, y, z]
        theta (float): rotational angle in radians

    Returns:
        array. Rotation matrix.
    """

    axis = np.array(list(axis))
    axis = axis / np.linalg.norm(axis)
    axis *= -np.sin(theta/2.0)
    a = np.cos(theta/2.0)
    b, c, d = tuple(axis.tolist())
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])


def align_axis(structure, axis='c', direction=(0, 0, 1)):
    """
    Rotates a structure so that the specified axis is along
    the [001] direction. This is useful for adding vacuum, and
    in general for using vasp compiled with no z-axis relaxation.

    Args:
        structure (Structure): Pymatgen Structure object to rotate.
        axis: Axis to be rotated. Can be 'a', 'b', 'c', or a 1x3 vector.
        direction (vector): Final axis to be rotated to.
    Returns:
        structure. Rotated to align axis along direction.
    """

    if axis == 'a':
        axis = structure.lattice._matrix[0]
    elif axis == 'b':
        axis = structure.lattice._matrix[1]
    elif axis == 'c':
        axis = structure.lattice._matrix[2]
    proj_axis = np.cross(axis, direction)
    if not(proj_axis[0] == 0 and proj_axis[1] == 0):
        theta = (
            np.arccos(np.dot(axis, direction)
            / (np.linalg.norm(axis) * np.linalg.norm(direction)))
        )
        R = get_rotation_matrix(proj_axis, theta)
        rotation = SymmOp.from_rotation_and_translation(rotation_matrix=R)
        structure.apply_operation(rotation)
    return structure


def get_structure_type(structure, write_poscar_from_cluster=False):
    """
    This is a topology-scaling algorithm used to describe the
    periodicity of bonded clusters in a bulk structure.

    Args:
        structure (structure): Pymatgen structure object to classify.
        write_poscar_from_cluster (bool): Set to True to write a
            POSCAR from the sites in the cluster.

    Returns:
        string. 'molecular' (0D), 'chain', 'layered', 'heterogeneous'
            (intercalated 3D), or 'conventional' (3D)
    """

    # The conventional standard structure is much easier to work
    # with.

    structure = SpacegroupAnalyzer(structure).get_conventional_standard_structure()

    # Noble gases don't have well-defined bonding radii.
    if not len([e for e in structure.composition
                if e.symbol in ['He', 'Ne', 'Ar', 'Kr', 'Xe']]) == 0:
        type = 'noble gas'
    else:
        if len(structure.sites) < 45:
            structure.make_supercell(2)

        # Create a dict of sites as keys and lists of their
        # bonded neighbors as values.
        sites = structure.sites
        bonds = {}
        for site in sites:
            bonds[site] = []

        for i in range(len(sites)):
            site_1 = sites[i]
            for site_2 in sites[i+1:]:
                if (site_1.distance(site_2) <
                            float(Element(site_1.specie).atomic_radius
                                      + Element(site_2.specie).atomic_radius) * 1.1):
                    bonds[site_1].append(site_2)
                    bonds[site_2].append(site_1)

        # Assimilate all bonded atoms in a cluster; terminate
        # when it stops growing.
        cluster_terminated = False
        while not cluster_terminated:
            original_cluster_size = len(bonds[sites[0]])
            for site in bonds[sites[0]]:
                bonds[sites[0]] += [
                    s for s in bonds[site] if s not in bonds[sites[0]]]
            if len(bonds[sites[0]]) == original_cluster_size:
                cluster_terminated = True

        original_cluster = bonds[sites[0]]

        if len(bonds[sites[0]]) == 0:  # i.e. the cluster is a single atom.
            type = 'molecular'
        elif len(bonds[sites[0]]) == len(sites): # i.e. all atoms are bonded.
            type = 'conventional'
        else:
            # If the cluster's composition is not equal to the
            # structure's overall composition, it is a heterogeneous
            # compound.
            cluster_composition_dict = {}
            for site in bonds[sites[0]]:
                if Element(site.specie) in cluster_composition_dict:
                    cluster_composition_dict[Element(site.specie)] += 1
                else:
                    cluster_composition_dict[Element(site.specie)] = 1
            uniform = True
            if len(cluster_composition_dict):
                cmp = Composition.from_dict(cluster_composition_dict)
                if cmp.reduced_formula != structure.composition.reduced_formula:
                    uniform = False
            if not uniform:
                type = 'heterogeneous'
            else:
                # Make a 2x2x2 supercell and recalculate the
                # cluster's new size. If the new cluster size is
                # the same as the old size, it is a non-periodic
                # molecule. If it is 2x as big, it's a 1D chain.
                # If it's 4x as big, it is a layered material.
                old_cluster_size = len(bonds[sites[0]])
                structure.make_supercell(2)
                sites = structure.sites
                bonds = {}
                for site in sites:
                    bonds[site] = []

                for i in range(len(sites)):
                    site_1 = sites[i]
                    for site_2 in sites[i+1:]:
                        if (site_1.distance(site_2) <
                                float(Element(site_1.specie).atomic_radius
                                + Element(site_2.specie).atomic_radius) * 1.1):
                            bonds[site_1].append(site_2)
                            bonds[site_2].append(site_1)

                cluster_terminated = False
                while not cluster_terminated:
                    original_cluster_size = len(bonds[sites[0]])
                    for site in bonds[sites[0]]:
                        bonds[sites[0]] += [
                            s for s in bonds[site] if s not in bonds[sites[0]]]
                    if len(bonds[sites[0]]) == original_cluster_size:
                        cluster_terminated = True

                if len(bonds[sites[0]]) != 4 * old_cluster_size:
                    type = 'molecular'
                else:
                    type = 'layered'

    if write_poscar_from_cluster:
        Structure.from_sites(original_cluster).to('POSCAR', 'POSCAR')

    return type

def write_potcar(pot_path=os.environ['PMG_VASP_PSP_DIR'], types='None', pseudopot='PBE'):
    """
    Writes a POTCAR file based on a list of types.
    Args:
        pot_path (str): can be changed to override default location
            of POTCAR files.
        types (list): list of same length as number of elements
            containing specifications for the kind of potential
            desired for each element, e.g. ['Na_pv', 'O_s']. If
            left as 'None', uses the defaults in the
            'potcar_symbols.yaml' file in the package root.
    """

    if pot_path == None:
        # This probably means the mpint_config.yaml file has not
        # been set up.
        pass
    else:
        poscar = open('POSCAR', 'r')
        lines = poscar.readlines()
        elements = lines[5].split()
        poscar.close()

        potcar_symbols = loadfn(
            os.path.join(PACKAGE_PATH, 'mat2d', 'potcar_symbols.yaml')
        )

        if types == 'None':
            sorted_types = [potcar_symbols[elt] for elt in elements]
        else:
            sorted_types = []
            for elt in elements:
                for t in types:
                    if t.split('_')[0] == elt:
                        sorted_types.append(t)

        potentials = []

        # Create paths, open files, and write files to
        # POTCAR for each potential.
        
        for potential in sorted_types:
            if pseudopot == 'PBE':
               potentials.append('{}/POT_GGA_PAW_PBE/{}/POTCAR'.format(pot_path, potential))
            elif pseudopot == 'LDA':
               potentials.append('{}/POT_LDA_PAW/{}/POTCAR'.format(pot_path, potential))
        outfile = open('POTCAR', 'w')
        for potential in potentials:
            infile = open(potential)
            for line in infile:
                outfile.write(line)
            infile.close()
        outfile.close()


def write_circle_mesh_kpoints(center=[0, 0, 0], radius=0.1, resolution=20):
    """
    Create a circular mesh of k-points centered around a specific
    k-point and write it to the KPOINTS file. Non-circular meshes
    are not supported, but would be easy to code. All
    k-point weights are set to 1.

    Args:
        center (list): x, y, and z coordinates of mesh center.
            Defaults to Gamma.
        radius (float): Size of the mesh in inverse Angstroms.
        resolution (int): Number of mesh divisions along the
            radius in the 3 primary directions.
    """

    kpoints = []
    step = radius / resolution

    for i in range(-resolution, resolution):
        for j in range(-resolution, resolution):
            if i**2 + j**2 <= resolution**2:
                kpoints.append([str(center[0]+step*i),
                                str(center[1]+step*j), '0', '1'])
    with open('KPOINTS', 'w') as kpts:
        kpts.write('KPOINTS\n{}\ndirect\n'.format(len(kpoints)))
        for kpt in kpoints:
            kpts.write(' '.join(kpt))
            kpts.write('\n')


def get_markovian_path(points):
    """
    Calculates the shortest path connecting an array of 2D
    points. Useful for sorting linemode k-points.

    Args:
        points (list): list/array of points of the format
            [[x_1, y_1, z_1], [x_2, y_2, z_2], ...]

    Returns:
        list: A sorted list of the points in order on the markovian path.
    """

    def dist(x, y):
        return math.hypot(y[0] - x[0], y[1] - x[1])

    paths = [p for p in it.permutations(points)]
    path_distances = [
        sum(map(lambda x: dist(x[0], x[1]), zip(p[:-1], p[1:])))
        for p in paths]
    min_index = np.argmin(path_distances)

    return paths[min_index]


def remove_z_kpoints():
    """
    Strips all linemode k-points from the KPOINTS file that include a
    z-component, since these are not relevant for 2D materials and
    slabs.
    """

    kpoint_lines = open('KPOINTS').readlines()

    twod_kpoints = []
    labels = {}
    i = 4

    while i < len(kpoint_lines):
        kpt_1 = kpoint_lines[i].split()
        kpt_2 = kpoint_lines[i+1].split()
        if float(kpt_1[2]) == 0.0 and [float(kpt_1[0]),
                                       float(kpt_1[1])] not in twod_kpoints:
            twod_kpoints.append([float(kpt_1[0]), float(kpt_1[1])])
            labels[kpt_1[4]] = [float(kpt_1[0]), float(kpt_1[1])]

        if float(kpt_2[2]) == 0.0 and [float(kpt_2[0]),
                                       float(kpt_2[1])] not in twod_kpoints:
            twod_kpoints.append([float(kpt_2[0]), float(kpt_2[1])])
            labels[kpt_2[4]] = [float(kpt_2[0]), float(kpt_2[1])]
        i += 3

    kpath = get_markovian_path(twod_kpoints)

    with open('KPOINTS', 'w') as kpts:
        for line in kpoint_lines[:4]:
            kpts.write(line)

        for i in range(len(kpath)):
            label_1 = [l for l in labels if labels[l] == kpath[i]][0]
            if i == len(kpath) - 1:
                kpt_2 = kpath[0]
                label_2 = [l for l in labels if labels[l] == kpath[0]][0]
            else:
                kpt_2 = kpath[i+1]
                label_2 = [l for l in labels if labels[l] == kpath[i+1]][0]

            kpts.write(' '.join([str(kpath[i][0]), str(kpath[i][1]), '0.0 !',
                                label_1]))
            kpts.write('\n')
            kpts.write(' '.join([str(kpt_2[0]), str(kpt_2[1]), '0.0 !',
                                label_2]))
            kpts.write('\n\n')

def check_errors(chkfile=None,logfile_name=None,jdirs=None,handlers=None):
    """
    Manual function to help check errors in job dirs 
    of a checkpoint file or in a list of job dirs 
    directly
    """
    logf = get_logger(logfile_name)
    if not handlers: 
       handlers = [VaspErrorHandler()]

    if chkfile:
        js = update_checkpoint(jfile=chkfile)
        chk_jobs = [j for j in jobs_from_file(chkfile) if not j.final_energy]
        err_chks = [check_job_with_custodian(job=j,logfile=logf,handlers=handlers) for j in chk_jobs]
        return err_chks
    elif jdirs:
        pass
     
def rerun_jobs(job_cmd=None, chkfiles=None, job_dirs=None):
    """
    Reruns the jobs after performing corrections by Custodian
    reading jobs either from checkpoint file (recommended) 
    or job directories. 
    """
    logR = get_logger('RerunJobReport')
    if chkfiles:
        checks  = [check_errors(chkfile=f) for f in chkfiles]
        CustodianReport = {'ErrorDir':[c['ErrorDir'][0] for c in sum(checks,[])],
                           'Error':[c['Error'][0] for c in sum(checks,[])],
                           'Correction':[c['Correction'][0] for c in sum(checks,[])]}
        pd.DataFrame(CustodianReport).to_csv('CustodianReport.csv')
        logR.info('Checks result is: {}'.format(checks))
        jobs = sum([jobs_from_file(f) for f in glob('*.json')],[])
        not_done_jobs = [j.job_dir for j in jobs if not j.final_energy]
        logR.info('There are {0} Not done jobs and they are {1}'.format(len(not_done_jobs),not_done_jobs))
        if job_cmd:
            for j in np.unique(not_done_jobs):
                os.chdir(j)
                os.system(job_cmd)
                os.chdir('../')
    if job_dirs:
        pass

def write_pbs_runjob(name, nnodes, nprocessors, pmem, walltime, binary):
    """
    writes a runjob based on a name, nnodes, nprocessors, walltime,
    and binary. Designed for runjobs on the Hennig group_list on
    HiperGator 1 (PBS).

    Args:
        name (str): job name.
        nnodes (int): number of requested nodes.
        nprocessors (int): number of requested processors.
        pmem (str): requested memory including units, e.g. '1600mb'.
        walltime (str): requested wall time, hh:mm:ss e.g. '2:00:00'.
        binary (str): absolute path to binary to run.
    """
    runjob = open('runjob', 'w')
    runjob.write('#!/bin/sh\n')
    runjob.write('#PBS -N {}\n'.format(name))
    runjob.write('#PBS -o test.out\n')
    runjob.write('#PBS -e test.err\n')
    runjob.write('#PBS -r n\n')
    runjob.write('#PBS -l walltime={}\n'.format(walltime))
    runjob.write('#PBS -l nodes={}:ppn={}\n'.format(nnodes, nprocessors))
    runjob.write('#PBS -l pmem={}\n'.format(pmem))
    runjob.write('#PBS -W group_list=hennig\n\n')
    runjob.write('cd $PBS_O_WORKDIR\n\n')
    runjob.write('mpirun {} > job.log\n\n'.format(binary))
    runjob.write('echo \'Done.\'\n')
    runjob.close()


def write_slurm_runjob(name, ntasks, pmem, walltime, binary):
    """
    writes a runjob based on a name, nnodes, nprocessors, walltime, and
    binary. Designed for runjobs on the Hennig group_list on HiperGator
    2 (SLURM).

    Args:
        name (str): job name.
        ntasks (int): total number of requested processors.
        pmem (str): requested memory including units, e.g. '1600mb'.
        walltime (str): requested wall time, hh:mm:ss e.g. '2:00:00'.
        binary (str): absolute path to binary to run.
    """

    nnodes = int(np.ceil(float(ntasks) / 32.0))

    runjob = open('runjob', 'w')
    runjob.write('#!/bin/bash\n')
    runjob.write('#SBATCH --job-name={}\n'.format(name))
    runjob.write('#SBATCH -o out_%j.log\n')
    runjob.write('#SBATCH -e err_%j.log\n')
    runjob.write('#SBATCH --qos=hennig-b\n')
    runjob.write('#SBATCH --nodes={}\n'.format(nnodes))
    runjob.write('#SBATCH --ntasks={}\n'.format(ntasks))
    runjob.write('#SBATCH --mem-per-cpu={}\n'.format(pmem))
    runjob.write('#SBATCH -t {}\n\n'.format(walltime))
    runjob.write('cd $SLURM_SUBMIT_DIR\n\n')
    runjob.write('module load intel/2016.0.109\n')
    runjob.write('module load openmpi/1.10.1\n')
    runjob.write('module load vasp/5.4.1\n\n')
    runjob.write('mpirun {} > job.log\n\n'.format(binary))
    runjob.write('echo \'Done.\'\n')
    runjob.close()

def process_to_dataframe(identifiers, metadata = ['energy','volume','kpoints'], chkfiles=glob('*.json'),job_dirs=None):
    """
    utility function that processes data from a list of checkpoints
    or directories into a pandas dataframe
 
    identifiers: Creates file names for the dataframes
                 1. dict type: job directory concatenation 
                example: {0:(('_',0),('/',1)),1:('__',1),'JoinBy':'_','OtherNames':'PBE'}
                         will split the job_dirs elements by
                         '_' and take position 0 followed by a split by '__' take
                         position 1 
                                           
    """
    if chkfiles:
       chk_jobs = sum([jobs_from_file(c) for c in chkfiles],[])
       energies = [j.final_energy for j in chk_jobs]

       if type(identifiers)==dict:

           def rec_split(string, split_rule):
               print (split_rule)
               for s in split_rule:
                   print (s)
                   string = string.split(s[0])[s[1]]
               return string
               
           dir_names = [j.job_dir for j in chk_jobs]
           print (list(identifiers.keys()))
           print (identifiers[0])
           dir_splits = [ [rec_split(d,identifiers[k]) for k in list(identifiers.keys()) \
                         if type(k)==int] for d in dir_names]
           dir_identifiers = [ identifiers['JoinBy'].join(d) for d in dir_splits]
           print (dir_identifiers)
           
           
def update_submission_template(submit_file):
    with open(submit_file,'r') as r:
       for l in r.readlines():
           if l.split('='):
               print (len(l.split('=')))
               var,val = l.split('=')[0], l.split('=')[1]
       print (var,val)
          


def parse_script():

    description = 'Input the checkpoint file or a list of directories enclosed in [..] or as a python glob'
    user_parser = ArgumentParser(description=description)

    user_parser.add_argument('-i', '--input', help='Input json file or a list of directories, see command man')
    user_parser.add_argument('-o', '--output', help='Output data file name in csv')
    if '.json' in sys.argv[2]:
        jdirs = [j.job_dir for j in jobs_from_file(sys.argv[2])]
    elif 'glob(' in sys.argv[2]:
        jdirs = glob('{}*'.format(sys.argv[2].replace('glob(', '').replace(')','')))
    elif '[' in sys.argv[2]:
        jdirs = sys.argv[2].replace('[','').replace(']','').split(',')
    output = sys.argv[4]

    return jdirs, output

