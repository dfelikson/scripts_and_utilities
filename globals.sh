#!/bin/sh

export dataDir=/disk/cg5/denis/CentralWestGrISGlaciers/Data

# ASP
export NTF=/disk/staff/gcatania/polar/Arctic/data/PGC/Rink_KS/stereo/NTF
export ASPscripts=/home/student/denis/CentralWestGrISGlaciers/Software/ASPscripts
export stereoDefaultFiles=$ASPscripts/stereoDefaultFiles
export ASP_DEMs=$dataDir/ASP_DEMs

# GIMP
export GIMP=$dataDir/GIMP
export gimpIceMask=$GIMP/GimpIceMask_15m_tile1_2.tif
export gimpOceanMask=$GIMP/GimpOceanMask_15m_tile1_2.tif
export gimpBedrockMask=$GIMP/GimpBedrockMask_90m.grd
#export gimpBedrockMask=$GIMP/GimpBedrockMask_90m_360m.grd

# ASTER
export AST14DMO=/disk/staff/gcatania/polar/Arctic/data/ASTER/AST14/AST14DMO
