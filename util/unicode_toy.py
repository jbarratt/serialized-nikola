#!/usr/bin/env python

import sys

myfile = open(sys.argv[1], 'r').read()

decoded = myfile.decode("windows-1252")

print decoded.encode('utf-8')
