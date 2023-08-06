#!/usr/bin/env python

from __future__ import division, unicode_literals, print_function, \
    absolute_import

"""
This script serves as a management tool for vasp projects, starting
from encut, kpoint or other parameter optimization of till the slab
solvation. Just define all types of calculations with their
corresponding specifications needed for the project in a yaml file
and run or rerun calculaitons as required.

Note: use your own materials project key to download the required
structure
"""

from six.moves import range

import os
import shutil
import yaml
from argparse import ArgumentParser
from fnmatch import fnmatch
from glob import glob
import ast

from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.io.vasp.inputs import Incar
from pymatgen.io.vasp.inputs import Potcar, Kpoints

from mpinterfaces import *
from mpinterfaces.utils import *
from mpinterfaces.mpint_parser import *
from mpinterfaces.workflows import *
from mpinterfaces.calibrate import Calibrate
from mpinterfaces.interface import Interface



MAPI_KEY = os.environ.get("MAPI_KEY", "")
vasp_config = {'twod_binary': VASP_TWOD_BIN,
               'bulk_binary': VASP_STD_BIN,
               'ncl_binary': VASP_NCL_BIN,
               'sol_binary': VASP_SOL_BIN,
               'custom_binary': VASP_CUSTOM_BIN}

def process_dir(val):
    poscar_list = []
    if os.path.isdir(val):
        for f in os.listdir(val):
            fname = os.path.join(val, f)
            if os.path.isfile(fname) and fnmatch(fname, "*POSCAR*"):
                poscar_list.append(Poscar.from_file(fname))
    return poscar_list


def process_input(args):
        if args.command == 'start_project':
           if args.i:
             f = open(args.i)
             my_project = yaml.load(open(args.i)) ## this will be the only CLI input
             f.close()
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

             error_handler = [VaspErrorHandler()]
             Order_WfNames = list(np.sort(list(WORKFLOWS['Steps'].keys())))
             steps_map = {'StepVASP0':StepVASP0,'StepVASP1':StepVASP1}
             steps_dict = {k:WORKFLOWS['Steps'][k]['TYPE'] for k in Order_WfNames}
             steps_map[steps_dict[list(steps_dict.keys())[0]]](my_project,struct_list)

             project_abs_dir = os.path.abspath(os.path.curdir)
             my_project['Project_Dir'] = project_abs_dir
             my_project['Running_Wflow'] = [Order_WfNames[0]]

             with open(args.i, 'w') as projfile:
                yaml.dump(my_project, projfile, default_flow_style=False)
             if os.path.exists('custodian.json'):
                os.remove('custodian.json')
             projfile.close()

        if args.command == 'continue_project':  
           if args.i:
             f = open(args.i)
             my_project = yaml.load(open(args.i)) ## this will be the only CLI input
             f.close()
             NAME = my_project['NAME']

             WORKFLOWS = my_project['Workflow']

             #error_handler = [VaspErrorHandler()]
             Order_WfNames = list(np.sort(list(WORKFLOWS['Steps'].keys())))
             steps_map = {'StepVASP0':StepVASP0,'StepVASP1':StepVASP1}
             steps_dict = {k:WORKFLOWS['Steps'][k]['TYPE'] for k in Order_WfNames}
             for k in Order_WfNames:
                if k not in my_project['Running_Wflow']:
                  steps_map[steps_dict[list(steps_dict.keys())[k]]](my_project)
                  orig_done = my_project['Running_Wflow']
                  orig_done.append(k)
                  my_project['Running_Wflow'] = orig_done
                  with open(args.i, 'w') as projfile:
                    yaml.dump(my_project, projfile, default_flow_style=False)
                  if os.path.exists('custodian.json'):
                    os.remove('custodian.json')
                  projfile.close()
                  break

        if args.command == 'check_project':
           # check if any input spec for the project 
           if args.i:
              f = open(args.i)
              project_spec = yaml.load(f)
              workflow_chkpts = glob('{}*.json'.format(project_spec['NAME']))
              print (workflow_chkpts)
              proj_dir = project_spec['Project_Dir']
              os.chdir(proj_dir)
              CustodianChecks=\
                {chk:check_errors(chkfile=chk,logfile_name=\
                     'Custodian_'+project_spec['NAME']) for chk in workflow_chkpts}
              with open('{}_CustodianReport.yaml'.format(project_spec['NAME']), 'w') as report:
                 yaml.dump(CustodianChecks, report, default_flow_style=False)
              report.close()      
              
        elif args.command == 'rerun_project':
           # Custodian yamls are input
           if args.i:
              f = open(args.i)
              rerun_spec = yaml.load(f)
              proj_dir = os.path.abspath(os.path.curdir)
              for k in list(rerun_spec.keys()):
                for case in rerun_spec[k]:
                   print ('Rerunning {}'.format(case['ErrorDir'][0]))
                   os.chdir(case['ErrorDir'][0])
                   os.system('sbatch submit_script')
                   os.chdir(proj_dir)
                      
              print ('Finished submitting reruns')

        elif args.command == 'analyze_project':
           # check for yaml analysis input for project
           if args.i:
              f = open(args.i)
              proj_spec = yaml.load(f)
              proj_wflow_st = proj_spec['Workflow']['Steps'] 
              for step in proj_wflow_st:
                if 'Analysis' in list(proj_wflow_st[step].keys()):
                   analyze_script = proj_wflow_st[step]['Analysis']['Script']
                   analyze_input = proj_wflow_st[step]['Analysis']['Input']
                   analyze_output = proj_wflow_st[step]['Analysis']['Output']
                   if '.py' in analyze_script:
                       os.system('python {0} -i {1} -o {2}'.format(analyze_script, analyze_input, analyze_output))
              print ('Analyzed the project according to specified post processing script')
              

        elif args.command == 'archive_project':
           # check for workflow.yaml input file 
           if args.i:
              print ('tar.gz the project json files, csvs and vasprun.xml files')
              f = open(args.i)
              proj_spec = yaml.load(f)
              name_spec = proj_spec['NAME']
              proj_dir = proj_spec['Project_Dir']
              os.chdir(proj_dir)
              os.system('tar cvzf {}*.json {}*.csv {}*.xml {}.tar.gz'.format(name_spec))

        elif args.command == 'load_settings':
           if args.i:
              user_dict = ast.literal_eval(args.i)
              if not os.path.exists(SETTINGS_FILE):
                 user_configs = {key:None for key in ['username','bulk_binary','twod_binary',\
                      'ncl_binary', 'sol_binary', 'custom_binary',\
                      'vdw_kernel','potentials','MAPI_KEY', 'queue_system', 'queue_template']}
                 with open(os.path.join(os.path.expanduser('~'),'.mpint_config.yaml'),'w') \
                   as config_file:
                         yaml.dump(user_configs, config_file, default_flow_style=False)
              config_data = yaml.load(open(SETTINGS_FILE))
              config_data.update(user_dict)
              load_config_vars(config_data)

def main():
   args = mpint_parse_arguments(sys.argv[1:])
   if args.command:
      process_input(args)
            
if __name__ == '__main__':
    main()
