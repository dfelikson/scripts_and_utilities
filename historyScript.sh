#!/bin/sh

#HISTFILE=~/.bash_history
#set -o history

#if [ $# -eq 0 ]; then
#   history
#else
#   historyFilename=".commandHistory_$1"
#   if [ -f $historyFilename ]; then
#      cat $historyFilename
#   fi
#fi

historyFilename=".commandHistory_$1"
if [ -f $historyFilename ]; then
   cat $historyFilename
fi

