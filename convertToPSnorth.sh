#!/bin/sh

geographicCoordsGRDFile=$1

filename=$(basename "$geographicCoordsGRDFile")
filename="${filename%.*}"

grdproject $geographicCoordsGRDFile -Js-45/90/70/1:1 -R-639955.000/855845.000/-3355595.000/-655595.000 -C -A -G$filename.ps.grd
grdreformat $filename.ps.grd $filename.ps.tif=gd:GTiff
exit

grd2xyz $geographicCoordsGRDFile | \
   /home/student/denis/GMT/bin/mapproject -Js-45/90/70/1:1 -R-2902500/2902500/-2902500/2902500 -F -C | \
   surface -G$filename.ps.grd -R-2902500/2902500/-2902500/2902500 -I1000

grdreformat $filename.ps.grd $filename.ps.tif=gd:GTiff

