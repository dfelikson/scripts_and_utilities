#!/bin/sh

dem1=$1
dem2=$2
outputDir=$3

dem1filename=`basename $dem1`
dem2filename=`basename $dem2`

#dem1epsg=`gdalinfo $dem1 | grep AUTHORITY | tail -1 | cut -d, -f2 | sed s/\"//g | sed s/]//g`
dem1proj4=`gdalsrsinfo $dem1 -o proj4`

eval "gdalwarp -overwrite -r bilinear -t_srs $dem1proj4 $dem2 $outputDir/${dem2filename%.*}_warped.tif"

