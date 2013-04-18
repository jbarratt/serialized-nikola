#!/usr/bin/env python

import sys
import os


def main():
    """
        Input: nikola posts directory
    """
    op_dir = sys.argv[1]

    for (dirpath, dirnames, filenames) in os.walk(op_dir):
        for f in filenames:
            if f != 'index.md':
                continue
            (base, slug) = os.path.split(dirpath)
            newfile = "%s/%s.md" % (base, slug)
            oldfile = "%s/%s" % (dirpath, f)
            print "moving %s to %s" % (f, newfile)
            with open(newfile, 'w') as nf:
                with open(oldfile, 'r') as of:
                    for l in of.readlines():
                        if l.startswith('.. slug'):
                            nf.write('.. slug: %s\n' % slug)
                        else:
                            nf.write(l)
                os.unlink(oldfile)
                os.rmdir(dirpath)

if __name__ == '__main__':
    main()
