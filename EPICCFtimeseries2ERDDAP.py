#!/usr/bin/env python

"""
 Background:
 --------
 EPICCFtimeseries2ERDDAP.py


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
parser.add_argument('sourcefile', metavar='sourcefile', type=str, help='path to .nc files')
parser.add_argument('timeseriesid', metavar='timeseriesid', type=str, help='station_name prefill value')
parser.add_argument("-adsg",'--add_dsg', type=str, 
                    help='''add global attribute field for discrete sampling geometry.
                    Options: point, timeSeries, trajectory, profile, timeSeriesProfile, trajectoryProfile''')

args = parser.parse_args()


"---"
df = EcoFOCI_netCDF(args.sourcefile)
global_atts = df.get_global_atts()
vars_dic = df.get_vars()
nchandle = df._getnchandle_()
data = df.ncreadfile_dic()

try :
    nchandle.createDimension('id_strlen',len(args.timeseriesid))
    nchandle.createVariable('station_id','S1',dimensions=('time','id_strlen'))
    nchandle.variables['station_id'].cf_role = 'timeseries_id'
    nchandle.variables['station_id'].long_name = 'timeseries_id'

except:
    print "{0} - not added".format('station_id')

#fill with default values
print args.timeseriesid
nchandle.variables['station_id'][:]=stringtochar(np.array(len(nchandle.dimensions['time']) * [args.fill_value]))


#add missing value attribute
for key,val in enumerate(vars_dic):
    nchandle.variables[val].fill_value = 1.0e35

df.close()
