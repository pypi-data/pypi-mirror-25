.. image:: https://travis-ci.org/henniggroup/MPInterfaces.svg?branch=master
.. image:: https://codecov.io/gh/henniggroup/MPInterfaces/coverage.svg?branch=master

MPinterfaces is a python package that enables high throughput Density
Functional Theory(DFT) analysis of arbitrary material interfaces(two dimensional
materials, hetero-structure, ligand capped
nanoparticles and surfaces in the presence of solvents) using
VASP_, VASPsol_, LAMMPS_, materialsproject_ database
as well as their open source tools_ and a little bit of ase_.

.. _materialsproject: https://github.com/materialsproject

.. _VASPsol: https://github.com/henniggroup/VASPsol

.. _VASP: http://www.vasp.at/

.. _tools: https://github.com/materialsproject

.. _LAMMPS: http://lammps.sandia.gov/

.. _ase: https://wiki.fysik.dtu.dk/ase/

.. image:: https://github.com/henniggroup/MPInterfaces/blob/master/docs/mpinterfaces-logo.png
   :width: 75 %
   :align: center

Installation
==============

Prepping - Setting up Virtual Environments
-------------------------------

We recommend setting up virtual environment
using Miniconda which can be installed according to their instructions from https://conda.io/miniconda.html

Follow the following steps to set up virtual environment using Miniconda

$ conda create -n name_of_your_environment python=3.6

On Windows:

$ activate name_of_your_environment

On Mac OS and Linux

$ source activate name_of_your_environment

$ conda install numpy

Note for HiperGator2:

As of now python/2.7.10 with gcc/5.2.0 has all the shared libraries
required for a successful installation.

Follow the following steps on HiperGator2:

$ module load gcc/5.2.0 python/2.7.10

Note: Use a virtualenv of version more than 15.1

$ python virtualenv.X.X.X/virtualenv.py <name_of_your_environment>

$ source name_of_your_environment/bin/activate

Get the latest version
-----------------------

If you already have a local copy, steps 1 and 2 of the following instructions
can be skipped. Just do a "git pull" from the MPInterfaces folder and go to
step 3(if the local copy was installed in the develop mode this step can be skipped too).

Note: on using virtual environments on your own machine, we recommend to use Miniconda.
On shared clusters that may have conflicts with shared libraries we recommend using virtualenv

1. Clone the latest version from github

  - git clone https://github.com/henniggroup/MPInterfaces.git

2. cd MPInterfaces

3. python setup.py install(or develop)

4. Copy the mpint_config.yaml file from config_files/mpint_config.yaml
   to mpinterfaces/mpint_config.yaml
   and update the file so that you have the following
   environment variables :

   - MAPI_KEY=the_key_obtained_from_materialsproject

   - VASP_PSP_DIR=path_to_vasp_potcar_files


How to Install Latest Pymatgen
-------------

See http://pymatgen.org/#getting-pymatgen


Documentation
==============

A very minimal documentation is avaiable at

http://henniggroup.github.io/MPInterfaces/

and work is underway to improve it.


Usage
==========

We use pymatgen tools for all structure manipulation tasks, so it would
be a good idea to start from here:

http://pymatgen.org/#using-pymatgen

The examples folder contain some sample scripts that demonstrate the
usage of mpinterfaces as well as materialsproject packages. For basic
usage please see **docs/usage.rst**.


Cite
======

If you use MPInterfaces for your work, please cite the paper: mpinterfaces-paper_

.. _mpinterfaces-paper: http://www.sciencedirect.com/science/article/pii/S0927025616302440


License
=======

MPInterfaces is released under the MIT License.::

    Copyright (c) 2014-2017 Henniggroup Cornell/University of Florida & NIST

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
    the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
    IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Contributing
=============

We try to follow the coding style used by pymatgen(PEP8):

http://pymatgen.org/contributing.html#coding-guidelines


Authors
=========

Kiran Mathew

Joshua Gabriel

Michael Ashton

Arunima Singh

Joshua T. Paul

Seve G. Monahan

Richard G. Hennig
