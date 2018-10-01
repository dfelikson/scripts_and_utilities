#!/bin/sh

geographicCoordsGRDFile=$1

filename=$(basename "$geographicCoordsGRDFile")
filename="${filename%.*}"

#grdproject $geographicCoordsGRDFile -Js0/-90/-71/1:1 -R-2902500/2902500/-2902500/2902500 -C -A -G$filename.ps.grd
#grdreformat $filename.ps.grd $filename.ps.tif=gd:GTiff

grd2xyz $geographicCoordsGRDFile | \
   /home/student/denis/Software/GMT/bin/mapproject -Js0/-90/-71/1:1 -R-2902500/2902500/-2902500/2902500 -F -C | \
   surface -G$filename.ps.grd -R-2902500/2902500/-2902500/2902500 -I2500

grdreformat $filename.ps.grd $filename.ps.tif=gd:GTiff

