"""
Objective:

Workflow steps overview:
1. Relax 2D and Bulk Competitors
2. Calculate Stability diagram
3. Prep a dummy IBZKPT
4. Run HSE band structure
5. Run +U calibrations
6. Run AFM calcualtions
7. Run Anisotropy calculations

"""

#### IMPORTS ####

##GENERAL python imports##
import os
import sys
from collections import OrderedDict
import yaml
from glob import glob

## MP imports ##
# Inputs
from pymatgen.io.vasp.inputs import Incar, Poscar
from pymatgen.io.vasp.inputs import Potcar, Kpoints
# Error handling
from custodian.vasp.handlers import VaspErrorHandler

## MPInterfaces calibrate engine imports
from mpinterfaces.calibrate import Calibrate
from mpinterfaces.utils import *
from mpinterfaces import *

import numpy as np

# vasp binaries
vasp_config = {'twod_binary': VASP_TWOD_BIN,
               'bulk_binary': VASP_STD_BIN,
               'ncl_binary': VASP_NCL_BIN,
               'sol_binary': VASP_SOL_BIN,
               'custom_binary': VASP_CUSTOM_BIN}



POTCAR_SPEC = yaml.load(open(PACKAGE_PATH+os.sep+'potcar_symbols.yaml'))

### STEP 1#####
def StepVASP0(my_project, struct_list):
    """
    1. reads a poscar list of a 2D motif(s)
    2. sets the default incar, kpoints and potcar as per mw
       database

    Returns:
        checkpoint Motif_like_2D_relax.json, Motif_like_bulk_relax.json
    """
    WORKFLOWS = my_project['Workflow']
    Workflow_Params = WORKFLOWS['Steps'][0]
    Workflow_name = Workflow_Params['NAME']
    job_dir = my_project['NAME'] + Workflow_Params['NAME']
    chkpt = job_dir + '.json'

    incar_dict = my_project['Incar_General']
    incar_init = Incar.from_dict(incar_dict)
    kpoints_init = Kpoints.monkhorst_automatic([18,18,18]) # an initialization to anything sensible

    # Decide the Kpoints density per atom setting here
    turn_knobs= OrderedDict({'POSCAR': struct_list,'KPOINTS':Workflow_Params['KPOINTS'],\
                             'POTCAR_pseudopotential':Workflow_Params['PSEUDOPOTENTIAL']})
    if Workflow_Params['Other_Knobs']:
        for k in Workflow_Params['Other_Knobs']: 
            turn_knobs.update(Workflow_Params['Other_Knobs'])
    job_bin = vasp_config[Workflow_Params['Queue']['Bin']]
    qdict = Workflow_Params['Queue']
    # Decide general queue settings for all runs in this step
    qadapter, job_cmd = get_run_cmmnd(partition=qdict['Partition'],ntasks=qdict['Ntasks'],\
                        nnodes = qdict['Nnodes'],walltime=qdict['Walltime'],job_bin=job_bin,\
                        mem=qdict['Memory'], job_name=job_dir)

    # run the jobs in this step
    run_cal(turn_knobs, qadapter, job_cmd, job_dir,
            chkpt, incar=incar_init, kpoints=kpoints_init,
            poscar=struct_list[0], is_matrix=Workflow_Params['Matrix'],\
            Grid_type=Workflow_Params['Kpt_Grid'])
    return [chkpt]

def StepVASP1(my_project):
   """
   performs a general VASP continuation step with the following actions:
   1. Uses relaxed CONTCARS of the Continue Source chkpt
   2. Updates the INCAR if so specified in the yaml file
   3. Updates the KPOINTS generation if so specified in the yaml
   4. Copies the necessary re-use files
   """
   WORKFLOWS = my_project['Workflow']
   Workflow_Params = WORKFLOWS['Steps'][1]
   Workflow_name = Workflow_Params['NAME']
   job_dir = my_project['NAME'] + Workflow_Params['NAME']
   chkpt = job_dir + '.json'
   prev_filter = Workflow_Params['Continue']['Filter']
   prev_chkpt = Workflow_Params['Continue']['Source']

   rerun_paths = continue_job_inputs(chkpt_files= prev_chkpt,\
    user_filters=prev_filter)
   reuse = Workflow_Params['Reuse']

   incar_init = Incar.from_file( rerun_paths[0]+os.sep+'INCAR' )
   kpoints_init = Kpoints.from_file( rerun_paths[0]+os.sep+'KPOINTS' )
   poscar_init = Poscar.from_file( rerun_paths[0]+os.sep+'POSCAR' )

   # Example update original INCAR (why? preserve settings like cutoff for this
   # step)
   incar_dict = incar_init.as_dict()
   incar_dict.update(Workflow_Params['Incar_Update'])
   incar = Incar.from_dict(incar_dict)

   # Update for Kpoints to be taken care of in run_cal's Grid_type

   turn_knobs = {'POSCAR': rerun_paths}

   job_bin = vasp_config[Workflow_Params['Queue']['Bin']]
   qdict = Workflow_Params['Queue']
   # Decide general queue settings for all runs in this step
   qadapter, job_cmd = get_run_cmmnd(partition=qdict['Partition'],ntasks=qdict['Ntasks'],\
                        nnodes = qdict['Nnodes'],walltime=qdict['Walltime'],job_bin=job_bin,\
                        mem=qdict['Memory'], job_name=job_dir)

   run_cal(turn_knobs, qadapter, job_cmd, job_dir,
            chkpt, incar=incar, kpoints=kpoints_init, poscar=poscar_init,
            reuse=True, is_matrix=False, Grid_type=Workflow_Params['Kpt_Grid'])

   return [chkpt]

def Non_VASP_Script(**kwargs):
   """
   performs an electronic structure prep calcaultion
   generating the optimized IBZKPT for HSE
   """

   chkpt = NAME+'_step3_wave.json'
   job_dir = NAME+"_step3_wave"

   rerun_paths = continue_job_inputs(chkpt_files=NAME+'_step2_nscf.json',\
    user_filters='To_Run.yaml')
   reuse = ['WAVECAR']

   incar_init = Incar.from_file( rerun_paths[0]+os.sep+'INCAR' )
   kpoints_init = Kpoints.from_file( rerun_paths[0]+os.sep+'KPOINTS' )
   poscar_init = Poscar.from_file( rerun_paths[0]+os.sep+'POSCAR' )

   # Example update original INCAR (why? preserve settings like cutoff for this
   # step)
   ### NEED TO SET INCAR setting to write out PARCHG file (what is it used for?)###

   incar_dict = incar_init.as_dict()
   Incar_Update_Settings = {'NSW': 0,
                            'ICHARG': 11,
                            'NEDOS': 2001,
                            'LCHARG':True,
                            'LAECHG':True,  # writes out files required for bader
                            'LWAVE':False }

   incar_dict.update(Incar_Update_Settings)
   incar = Incar.from_dict(incar_dict)

   turn_knobs = {'POSCAR': rerun_paths}

   job_bin = twod_bin
   qadapter, job_cmd = get_run_cmmnd(ntasks=16, walltime='01:00:00',\
                         job_bin=job_bin, mem=1000, job_name=NAME)

   run_cal(turn_knobs, qadapter, job_cmd, job_dir,
            chkpt, incar=incar_init, kpoints=kpoints_init, poscar=poscar_init,
            reuse=True, is_matrix=False, Grid_type=KPOINTS_GENERAL['Method'],
            mappings_override = potcar_dict )

   return [chkpt]

def process_to_dataframe(chkpts, tags=['final_energy', 'job_name']):
    """
    general post-processing tool that will
    make use of MPInterfaces measurement module
    taking a list of checkpoint files
    and performing MeasurementAnalysis tasks on the
    concerned files as dictated by the tags
    Args:
        chkpts: (list) of checkpoint files
        tags : (list) of properties of interest
               Eg: final_energy (default), job_name,
                   band_gap
                   effective_mass, magnetization_orbs
                   magnetization_total
    """

    pass

def run_cal(turn_knobs, qadapter, job_cmd, job_dir, checkpoint_file,
            incar=None, poscar=None, potcar=None, kpoints=None, reuse=None,
            Grid_type='G',pseudopotential='PBE',is_matrix=True, cal_type='Cal', reuse_incar = None,
            n_layers=None, magnetism=False, database=None, mappings_override=POTCAR_SPEC):
    """
    calibrate job launching function
    """
    cal = Calibrate(incar, poscar, potcar, kpoints, reuse=reuse,
                    reuse_incar = reuse_incar, is_matrix=is_matrix,
                    turn_knobs=turn_knobs, qadapter=qadapter,
                    job_cmd = job_cmd, job_dir=job_dir, reuse_override = False,
                    Grid_type=Grid_type,pseudopotential=pseudopotential,magnetism=magnetism,
                    checkpoint_file=checkpoint_file, cal_logger=logger, database=database,
                    mappings_override=mappings_override)
    cal.setup()
    cal.run()

if __name__=='__main__':
    """
    Workflow interface with input yaml and
    construction of sequence
    """

    ## Most General inputs for the project from
    # project.yaml

    my_project = yaml.load(open('my_project.yaml')) ## this will be the only CLI input

    NAME = my_project['NAME']

    INCAR_GENERAL = my_project['Incar_General']
    POTCAR_SPEC = yaml.load(open(my_project['Potcar_Spec']))

    MATERIALS_LIST = my_project['Insilico_Fab']['Material_List']
    struct_list = [Poscar.from_file(poscar) for poscar in glob('StructsDir/POSCAR*') \
                   if 'StructsDir' in MATERIALS_LIST] + \
                  [Poscar(get_struct_from_mp(p)) for p in MATERIALS_LIST \
                   if 'StructsDir' not in p]

    WORKFLOWS = my_project['Workflow']
    
    project_log=get_logger(NAME+"_InSilico_Materials")

    # general structure creation manipulation module , for example make slabs
    # make 2D material, or use a different source like GASP as well
    # insilico_fab(creator = SYNTH['creator'], script=SYNTH['script'])

    error_handler = [VaspErrorHandler()]
    steps= my_project['Workflow']['Steps'].keys() # testing [Relax]
    #print (steps)
    #print (struct_list)
    #print ('Reached past steps')
    Relax()

    #launch_daemon([Relax], interval=30,handlers=error_handler, ld_logger=project_log)
