#!/usr/bin/env python

"""
 Background:
 --------
 EPICCFgliderprofile2ERDDAP.py


 Purpose:
 --------
 Add a variable to a netcdf file

 History:
 --------

 2016-06-10: Update program so that it pulls possible new variables from epic.json file
 2016-08-10: transfer routine to EcoFOCI_MooringAnalysis package to simplify and unify

"""

#System Stack
import datetime
import argparse
import os

#Science Stack
from netCDF4 import Dataset
from netCDF4 import stringtochar
import numpy as np

#User Defined Stack
from io_utils import ConfigParserLocal
from io_utils.EcoFOCI_netCDF_read import EcoFOCI_netCDF


__author__   = 'Shaun Bell'
__email__    = 'shaun.bell@noaa.gov'
__created__  = datetime.datetime(2014, 01, 29)
__modified__ = datetime.datetime(2016, 8, 10)
__version__  = "0.2.0"
__status__   = "Development"
__keywords__ = 'netCDF','meta','header'



"""------------------------------- MAIN------------------------------------------------"""

parser = argparse.ArgumentParser(description='convert netcdf file to erddap formatted file')
parser.add_argument('sourcefile', 
    metavar='sourcefile', 
    type=str, 
    help='path to .nc files')
parser.add_argument("cdm_data_type",
    metavar='cdm_data_type', 
    type=str, 
    help='''add global attribute field for discrete sampling geometry.
            Options: Point, TimeSeries, Trajectory, 
            Profile, TimeSeriesProfile, TrajectoryProfile''')

args = parser.parse_args()

def choose_cdm(cdm_type=None):
    if cdm_type in ['Point']:
        cf_role = None
    elif cdm_type in ['Profile']:
        cf_role = 'profile_id'
    elif cdm_type in ['TimeSeries']:
        cf_role = 'timeseries_id'
    elif cdm_type in ['TimeSeriesProfile']:
        cf_role = 'profile_id'
    elif cdm_type in ['Trajectory']:
        cf_role = 'trajectory_id'
    elif cdm_type in ['TrajectoryProfile']:
        cf_role = 'profile_id'
    else:
        cf_role = None

"---"
df = EcoFOCI_netCDF(args.sourcefile)
global_atts = df.get_global_atts()
vars_dic = df.get_vars()
nchandle = df._getnchandle_()
data = df.ncreadfile_dic()

cf_role = choose_cdm(args.adsg)

try :
    nchandle.createDimension('id_strlen',len(args.trajectoryid))
    nchandle.createVariable('trajectoryid','S1',dimensions=('record_number','id_strlen'))
    nchandle.variables['trajectoryid'].cf_role = 'trajectory_id'
    nchandle.variables['trajectoryid'].long_name = 'trajectory_id'

except:
    print "{0} - not added".format('trajectoryid')

#fill with default values
print args.trajectoryid
nchandle.variables['trajectoryid'][:]=stringtochar(np.array(len(nchandle.dimensions['record_number']) * [args.trajectoryid]))


#add missing value attribute
for key,val in enumerate(vars_dic):
    nchandle.variables[val].fill_value = 1.0e35


    
df.close()
