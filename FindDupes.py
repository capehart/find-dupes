#!/usr/bin/env python

"""
FindDupes.py is intended to search a large(ish) tree to find duplicate files.
The original impetus was a disorganzied music directory that was accessed by
the sqeezebox producing too many plays of the same song.

@author capehart
@date 2012-06-05

@usage:
FindDupes.py /path/to/root

@requires: Python 2.7 (for argparse)
"""

import argparse
import logging
import md5file
import os
import sys

class DupeFinder:
    
    def print_dupes(self, dupes):
        logging.debug('Printing the found duplicates...')
        for (key,value) in dupes.items():
            print "%s:" % (key)
            for path in value:
                print "\t%s" % (path)
            

    def find_duplicates(self, root_path):
        """
        find_duplicates searches a path for files with the same md5sum and
        returns a list of those duplicate files.
        """
        logging.info('Looking for duplicates in %s' % (root_path))
        #First, build the dictionary of sets of everything seen
        seen = {}
        for dirpath, dirs, files in os.walk(root_path,followlinks=self.args.follow):
            logging.info("Processing directory: %s" % (dirpath))
            for file in files:
                full_path = os.path.join(dirpath,file)
                logging.debug("Processing file: %s" % (full_path))
                md5sum = md5file.md5sum(full_path)
                logging.debug("Calculated md5 hash %s for file %s" % (md5sum, full_path))
                if md5sum in seen.keys():
                    logging.debug("%s has already been seen. Adding %s to the set." % (md5sum, full_path))
                    seen[md5sum].add(full_path)
                else:
                    logging.debug("%s is a new sum." % (md5sum))
                    seen[md5sum] = set([full_path])
                    
        #Then in the dictionary of sets, select those keys for which there is more than one value in the set
        dupes = {}
        for (key,value) in seen.items():
            if len(value) > 1:
                dupes[key] = value
        return dupes

    def main(self, argv=None ):
        """
        Main's purpose is to extract the path from the command line (or other) 
        arguments and then pass that to the dupe-finder.
        """

        if argv == None:
            argv = sys.argv
        parser = argparse.ArgumentParser(description='Find duplicate files in a tree by comparing md5 sums.')
        parser.add_argument('path', metavar='/Root/Path', help='The root level directory under which you\'d like to find duplicates.', default=None)
        parser.add_argument('-f', dest='follow', help='Follow Symlinks', action='store_true', default=False)
        parser.add_argument('-v', dest='verbose', help='Verbosity from 1(quiet)(default) to 3(chatty)', action='store', default=1)
        parser.add_argument('-l', dest='log_path', help='logging path', action='store', default=None)
        parser.add_argument('-c', dest='log_console', help='log information to the console. (If false [default], only the duplicate files are output.)', action='store_true', default=False)
        self.args = parser.parse_args()
        
        loglevel = logging.WARNING
        if self.args.log_path or self.args.log_console:
            if int(self.args.verbose) == 1:
                loglevel = logging.WARNING
            elif int(self.args.verbose) == 2:
                loglevel = logging.INFO
            elif int(self.args.verbose) == 3:
                loglevel = logging.DEBUG

            if self.args.log_path:
                logging.basicConfig(filename=self.args.log_path, 
                                    format='%(asctime)s %(levelname)s: %(message)s', 
                                    level=loglevel)
                logging.info('Turned on File Logger.')

            if self.args.log_console:
                log_console_format = '%(message)s'
                if self.args.log_path:
                    console = logging.StreamHandler()
                    console.setLevel(loglevel)
                    console.setFormatter(logging.Formatter(log_console_format))
                    logging.getLogger('').addHandler(console)
                else:
                    logging.basicConfig(level=loglevel, format=log_console_format)

                logging.info('Turned on Console Logger.')

                
        duplicate_paths = self.find_duplicates(self.args.path)
        self.print_dupes(duplicate_paths)


if __name__ == '__main__':
    df = DupeFinder()
    sys.exit(df.main())
