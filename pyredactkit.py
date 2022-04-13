#!/usr/bin/env python
"""
Utility to redact sensitive data
"""

import argparse
from src.redact import Redactor
import os
import sys
import glob


def main():

    parser = argparse.ArgumentParser(description='Read in a file or set of files, and return the result.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("path", nargs="+",
                        help="Path of a file or a directory of files")
    parser.add_argument(
        "-t", "--redactiontype", help="""Type of data to redact. 
        dns,
        emails,
        ipv4,
        ipv6""")
    parser.add_argument(
        "-o", "--outdir", help="Output directory of the file")
    parser.add_argument('-r', '--recursive', action='store_true',
                        default=True, help='Search through subfolders')
    parser.add_argument('-e', '--extension', default='',
                        help='File extension to filter by.')
    args = parser.parse_args()

    full_paths = [os.path.join(os.getcwd(), path) for path in args.path]
    files = set()

    for path in full_paths:
        if os.path.isfile(path):
            fileName, fileExt = os.path.splitext(path)
            if args.extension == '' or args.extension == fileExt:
                files.add(path)
        else:
            if (args.recursive):
                full_paths += glob.glob(path + '/*')

    # redact file
    redact_obj = Redactor()

    for file in files:
        if args.redactiontype:
            redact_obj.process_file(file, args.redactiontype)
        elif args.outdir:
            redact_obj.process_file(file, args.redactiontype, args.outdir)
        else:
            redact_obj.process_file(file)


if __name__ == "__main__":
    main()
