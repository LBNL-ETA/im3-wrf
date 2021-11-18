'''
@Xuan Luo (xuanluo@lbl.gov)

single E plus model run

usage: run_eplus <Building ID> <E plus model name> <E plus working folder >

'''

import argparse
import os
from subprocess import run
from subprocess import call


# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')

# Required positional argument

parser.add_argument('model_name', type=str,
                    help='Building EnergyPlus model name')

parser.add_argument('work_folder', type=str,
                    help='Building EnergyPlus work folder')

parser.add_argument('epw_name', type=str,
                    help='Weather file name')

parser.add_argument('prefix', type=str,
                    help='Result prefix')

args = parser.parse_args()

model_name = args.model_name
work_folder = args.work_folder
idf_name = os.path.join(work_folder, model_name + ".idf")
epw_name =  args.epw_name
prefix = args.prefix


if os.path.isdir(work_folder) and os.path.exists(idf_name):
    run(['mkdir', os.path.join(work_folder, prefix)])
    run(['./EnergyPlus-9-4-0/energyplus-9.4.0', '-w', epw_name, '-d', os.path.join(work_folder, prefix), os.path.join(idf_name)])