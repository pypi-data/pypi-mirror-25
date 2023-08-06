from pymatgen.io.vasp.outputs import Vasprun, Outcar
from mpinterfaces.utils import jobs_from_file, parse_script, print_exception
import pandas as pd
import numpy as np

if __name__ == '__main__':
    
    process_dirs, output = parse_script()
    data = {'Name':[]}
    # your data processing to create a dictionary of lists of data 
    # example: data['your_property'].append()
    data.update({k : [] for k in user_properties})
    for p in process_dirs:
        try:
           ## your data extraction process
           # example: v = Vasprun(p+'/vasprun.xml')
           print (p)
        except:
           print (p, print_exception())

    pd.DataFrame(data).to_csv('{}.csv'.format(output) ,index=False)
