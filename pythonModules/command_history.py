
import os
import time


def save_command_history(argsList, overwrite=False):
   historyFilename = '.commandHistory_' + os.path.basename(argsList[0])

   # Check if a command history file exists
   if not os.path.isfile(historyFilename) or overwrite:
      f = open(historyFilename, 'w')
   else:
      f = open(historyFilename, 'a')

   # Output
   f.write(time.strftime('%d%b%Y  %H:%M:%S  '))
   f.write(' '.join(argsList))
   f.write('\n')
   f.close()


def get_command_history(filename):
   historyFilename = '.commandHistory_' + filename

   if not os.path.isfile(historyFilename):
      print ''
   else:
      with open(historyFilename, 'r') as fin:
          print fin.read()

