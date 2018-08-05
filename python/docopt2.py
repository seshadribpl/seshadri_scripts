#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" docopt_example.py
    
    Usage:
        docopt_example.py -h
        docopt_example.py <action> [-u | -f  ]
    Options:
        -h,--help        : show this help message
        action           : can be display or post
        -u,--user-list   : list of users IDs
        -f,--filesystem  : nfs filesystem name
        
"""
# the above is our usage string that docopt will read and use to determine
# whether or not the user has passed valid arguments.
# import the docopt function from the docopt module
from docopt import docopt


def main(docopt_args):
    """ main-entry point for program, expects dict with arguments from docopt() """
    
    
    
    # User passed the required argument
    if docopt_args["<action>"]:
        print "You have used the required argument: " + docopt_args["<action>"]
        
        # Get flags used
        if docopt_args["--user-list"]:
            print "   with --user-list\n"
        elif docopt_args["--filesystem"]:
            print "   with --filesystem\n"
        
        else:
            print "   with no flags.\n"
    
# START OF SCRIPT
if __name__ == "__main__":
    # Docopt will check all arguments, and exit with the Usage string if they
    # don't pass.
    # If you simply want to pass your own modules documentation then use __doc__,
    # otherwise, you would pass another docopt-friendly usage string here.
    # You could also pass your own arguments instead of sys.argv with: docopt(__doc__, argv=[your, args])
    args = docopt(__doc__)
    # We have valid args, so run the program.
    main(args)