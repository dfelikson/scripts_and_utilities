#!/bin/bash

pid=$1

pidcheck="ps ax | awk '{if (\$1==$pid) print}'"
result=`eval $pidcheck`

if [ -z "$result" ]; then
   echo "$pid is not running on `hostname -s`!" | mail -s "$pid finished" denis.felikson@utexas.edu
fi

