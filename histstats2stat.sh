#!/bin/sh

infile=$1
stat=$2

str=`grep $stat $infile`
if [ -z "$str" ]; then
    echo "NaN"
else
    echo $str | cut -d":" -f2 | tr -d ' '
fi

