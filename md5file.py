#!/usr/bin/env python

import argparse
import hashlib
import sys

def md5sum(filename ):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(2**20), b''):
            md5.update(chunk)
    return md5.hexdigest()

def main(argv=None):
    if argv == None:
        argv = sys.argv
    parser = argparse.ArgumentParser(description='Get the MD5 sum of a file.')
    parser.add_argument('file', metavar='/path/to/file', help='The root level directory under which you\'d like to find duplicates.', default=None)
    args = parser.parse_args()
    md5sum(args.file)

if __name__ == '__main__':
    sys.exit(md5sum())
