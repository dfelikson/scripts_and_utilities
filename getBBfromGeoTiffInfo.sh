#!/bin/sh

infoFile=$1

BBxMin=`cat $infoFile | grep "Upper Left"  | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1`
BBxMax=`cat $infoFile | grep "Upper Right" | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f1`
BByMin=`cat $infoFile | grep "Lower Left"  | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2`
BByMax=`cat $infoFile | grep "Upper Left"  | cut -d "(" -f2 | cut -d ")" -f1 | cut -d "," -f2`

echo BBxMin: $BBxMin
echo BBxMax: $BBxMax
echo BByMin: $BByMin
echo BByMax: $BByMax
