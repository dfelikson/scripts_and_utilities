#!/bin/sh
source ~/ScriptsAndUtilities/globals.sh

# Setup
dem1=$1
dem2=$2
outputDir=$3
interpMethod=$4

if [ "$interpMethod" == "" ]; then
   interpMethod="bilinear"
fi

dem1Path=$(dirname "$dem1")
dem2Path=$(dirname "$dem2")
dem1Filename=$(basename "$dem1")
dem2Filename=$(basename "$dem2")
dem1Filename="${dem1Filename%.*}"
dem2Filename="${dem2Filename%.*}"


# Processing
# Get bounding box for DEM 1
demBBupperleft=`gdalinfo $dem1  | grep "Upper Left"`
demBBlowerleft=`gdalinfo $dem1  | grep "Lower Left"`
demBBupperright=`gdalinfo $dem1 | grep "Upper Right"`
demBBlowerright=`gdalinfo $dem1 | grep "Lower Right"`
demBBxMin1=`echo $demBBupperleft  | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1 | tr -d ' '`
demBBxMax1=`echo $demBBupperright | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1 | tr -d ' '`
demBByMin1=`echo $demBBlowerleft | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | tr -d ' '`
demBByMax1=`echo $demBBupperleft | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | tr -d ' '`
pixelSize1=`gdalinfo $dem1 | grep "Pixel Size"`
demPixelSizeX1=`echo $pixelSize1 | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1`
demPixelSizeY1=`echo $pixelSize1 | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | sed 's/-//'`

# Get bounding box for DEM 2
demBBupperleft=`gdalinfo $dem2  | grep "Upper Left"`
demBBlowerleft=`gdalinfo $dem2  | grep "Lower Left"`
demBBupperright=`gdalinfo $dem2 | grep "Upper Right"`
demBBlowerright=`gdalinfo $dem2 | grep "Lower Right"`
demBBxMin2=`echo $demBBupperleft  | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1 | tr -d ' '`
demBBxMax2=`echo $demBBupperright | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1 | tr -d ' '`
demBByMin2=`echo $demBBlowerleft | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | tr -d ' '`
demBByMax2=`echo $demBBupperleft | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | tr -d ' '`
pixelSize2=`gdalinfo $dem2 | grep "Pixel Size"`
demPixelSizeX2=`echo $pixelSize2 | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1`
demPixelSizeY2=`echo $pixelSize2 | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | sed 's/-//'`

# Find overlapping region
if [ `echo "$demBBxMin1 > $demBBxMin2" | bc -l` == "1" ]; then
   demBBxMin=$demBBxMin1
else
   demBBxMin=$demBBxMin2
fi
if [ `echo "$demBBxMax1 < $demBBxMax2" | bc -l` == "1" ]; then
   demBBxMax=$demBBxMax1
else
   demBBxMax=$demBBxMax2
fi

if [ `echo "$demBByMin1 > $demBByMin2" | bc -l` == "1" ]; then
   demBByMin=$demBByMin1
else
   demBByMin=$demBByMin2
fi
if [ `echo "$demBByMax1 < $demBByMax2" | bc -l` == "1" ]; then
   demBByMax=$demBByMax1
else
   demBByMax=$demBByMax2
fi

# Find the higher-resolution DEM and select interpolation method
if [ "$interpMethod" == "automatic" ]; then
   check=$(awk 'BEGIN{ print "'$demPixelSizeX1'"<"'$demPixelSizeX2'" }')
   if [ "$check" -eq 1 ]; then
      interpMethod=average
   else
      interpMethod=bilinear
   fi
fi

# Select overlapping region from DEM 1
echo selecting overlapping region from DEM 1
sh preprocessDEM.sh $dem1 $outputDir tif N/A
gdal_translate -projwin $demBBxMin $demBByMax $demBBxMax $demBByMin $outputDir/$dem1Filename.tif $outputDir/${dem1Filename}_select.tif

# Interpolate DEM 2 to points in DEM 1
echo interpolating DEM 2 to DEM 1 grid
demBBupperleft=`gdalinfo $outputDir/${dem1Filename}_select.tif  | grep "Upper Left"`
demBBlowerleft=`gdalinfo $outputDir/${dem1Filename}_select.tif  | grep "Lower Left"`
demBBupperright=`gdalinfo $outputDir/${dem1Filename}_select.tif | grep "Upper Right"`
demBBlowerright=`gdalinfo $outputDir/${dem1Filename}_select.tif | grep "Lower Right"`
demBBxMin1=`echo $demBBupperleft  | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1 | tr -d ' '`
demBBxMax1=`echo $demBBupperright | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1 | tr -d ' '`
demBByMin1=`echo $demBBlowerleft | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | tr -d ' '`
demBByMax1=`echo $demBBupperleft | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | tr -d ' '`
#pixelSize1=`gdalinfo $dem1 | grep "Pixel Size"`
pixelSize1=`gdalinfo $outputDir/${dem1Filename}_select.tif | grep "Pixel Size"`
demPixelSizeX1=`echo $pixelSize1 | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1`
demPixelSizeY1=`echo $pixelSize1 | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2 | sed 's/-//'`

rgn="-R$demBBxMin1/$demBBxMax1/$demBByMin1/$demBByMax1"

sh preprocessDEM.sh $dem2 $outputDir tif N/A
#gdalwarp -overwrite -r $interpMethod -srcnodata -9999 -dstnodata -9999 \
#   -te $demBBxMin1 $demBByMin1 $demBBxMax1 $demBByMax1 -tr $demPixelSizeX1 $demPixelSizeY1 \
#   -multi -wo NUM_THREADS=ALL_CPUS \
#   $outputDir/$dem2Filename.tif $outputDir/${dem2Filename}_select.tif
   
gdalwarp -overwrite -r $interpMethod -te $demBBxMin1 $demBByMin1 $demBBxMax1 $demBByMax1 -tr $demPixelSizeX1 $demPixelSizeY1 -multi -wo NUM_THREADS=ALL_CPUS $outputDir/$dem2Filename.tif $outputDir/${dem2Filename}_select.tif

