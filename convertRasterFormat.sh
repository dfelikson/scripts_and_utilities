#!/bin/sh

# Setup
raster=$1
outputDir=$2
reformat=$3
reproject=$4


# Processing
rasterPath=$(dirname "$raster")
rasterFilename=$(basename "$raster")
rasterExtension="${rasterFilename##*.}"
rasterFilename="${rasterFilename%.*}"

# Reformat
if [ "$reformat" == "grd" ]; then
   if [ -f $outputDir/$rasterFilename.grd ]; then
      echo $outputDir/$rasterFilename.grd already exists
   elif [ "$rasterExtension" == "grd" ]; then
      echo copying $raster to $outputDir
      cp $raster $outputDir
   else
      echo converting $raster to GMT format
      gdal_translate -of GMT -a_nodata -9999 $raster $outputDir/$rasterFilename.grd
      #grdreformat $raster=gd:GTiff $outputDir/$rasterFilename.grd
   fi
fi
if [ "$reformat" == "tif" ]; then
   if [ -f $outputDir/$rasterFilename.tif ]; then
      echo $outputDir/$rasterFilename.tif already exists
   elif [ "$rasterExtension" == "tif" ]; then
      echo copying $raster to $outputDir
      cp $raster $outputDir
   else
      echo converting $raster to GTiff format
      
      # Change nans to -9999
      grdmath $raster ISNAN -9999 $raster IFELSE = $outputDir/temp1.grd

      # Convert format
      grdreformat $outputDir/temp1.grd $outputDir/temp2.grd=cf # Necessary because GMT 5 grid files are not compatible
                                                               # with whatever version of GDAL we have.
      gdal_translate -a_nodata -9999 -of GTiff \
         -a_srs '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=-45 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs' \
         $outputDir/temp2.grd $outputDir/$rasterFilename.tif

      # Cleanup
      \rm -f $outputDir/temp*.grd
   fi
fi

# Reproject

