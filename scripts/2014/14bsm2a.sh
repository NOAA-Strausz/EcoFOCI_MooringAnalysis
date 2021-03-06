#!/bin/bash

data_dir="/Volumes/WDC_internal/Users/bell/ecoraid/"
prog_dir="/Volumes/WDC_internal/Users/bell/Programs/Python/EcoFOCI_MooringAnalysis/"

mooringID='14bsm2a'
mooringYear='2014'
lat='56 52.067 N'
lon='164 03.033 W'
site_depth=71
deployment_date='2014-05-09 07:00:00'
recovery_date='2014-10-19 19:15:00'

echo $prog_dir
echo $mooringID
echo $mooringYear
echo $lat $lon
echo $site_depth

echo "-------------------------------------------------------------"
echo "SBE37 Processing"
echo "-------------------------------------------------------------"

serial_no=2327
input=${data_dir}${mooringYear}/Moorings/${mooringID}/raw/sbe37/14bsm2a_sbe37_2327_0061.asc
output=${data_dir}${mooringYear}/Moorings/${mooringID}/working/14bsm2a_s37_0061m.unqcd.nc
python ${prog_dir}EcoFOCIraw2nc.py ${input} ${output} s37 0061 -kw True -latlon $lat $lon -add_meta $mooringID $serial_no $site_depth
python ${prog_dir}NetCDF_Trim.py ${output} -sd ${deployment_date} -ed ${recovery_date}
