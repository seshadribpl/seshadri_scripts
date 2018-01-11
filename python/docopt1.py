#!/usr/bin/env python

'''

Usage: 
  dostuff.py listfile <path> 
  dostuff.py changedir <path>
  dostuff cat <path>
  dostuff remove <path>

# Arguments:
#   listfile  list a file
#   changedir change into a directory
#   cat       print a file's contents
#   remove    delete a file

Examples:
  dostuff.py listfile /etc/inittab
  dostuff.py changedir /tmp
  dostuff.py cat /etc/mtab
  dostuff.py remove /etc/resolv.conf

Options:
  -h, --help
  -l FILE --listfile=FILE       list a file
  -d DIR --changedir=DIR        change into a directory
  -c FILE --cat=FILE            print a file's contents
  -r FILE --remove=FILE         delete a file

'''

from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)




