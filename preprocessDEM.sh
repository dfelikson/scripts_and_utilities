#!/bin/sh

# Setup
dem=$1
outputDir=$2
reformat=$3
reproject=$4


# Processing
demPath=$(dirname "$dem")
demFilename=$(basename "$dem")
demExtension="${demFilename##*.}"
demFilename="${demFilename%.*}"

# Reformat
if [ "$reformat" == "grd" ]; then
   if [ -f $outputDir/$demFilename.grd ]; then
      echo $outputDir/$demFilename.grd already exists
   elif [ "$demExtension" == "grd" ]; then
      echo copying $dem to $outputDir
      cp $dem $outputDir
   else
      echo converting $dem to GMT format
      #gdal_translate -of GMT -a_nodata -9999 $dem $outputDir/$demFilename.grd
      grdreformat $dem=gd:GTiff $outputDir/$demFilename.grd
   fi
fi
if [ "$reformat" == "tif" ]; then
   if [ -f $outputDir/$demFilename.tif ]; then
      echo $outputDir/$demFilename.tif already exists
   elif [ "$demExtension" == "tif" ]; then
      echo copying $dem to $outputDir
      cp $dem $outputDir
   else
      echo converting $dem to GTiff format
      grdreformat $dem $outputDir/temp.grd=cf # Necessary because GMT 5 grid files are not compatible
                                              # with whatever version of GDAL we have.
      gdal_translate -a_nodata nan -of GTiff $outputDir/temp.grd $outputDir/$demFilename.tif
      \rm $outputDir/temp.grd
   fi
fi

# Reproject


