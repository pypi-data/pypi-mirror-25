from __future__ import print_function

from . import utl

import errno
import os
import sys

# wouldn't need this in python3
def mkpath(path):
    """makedirs but ignore "already exists" error """
    try:
        os.makedirs(path)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise

def load_value(filename):
    """load single value from file"""
    with open(filename, "rb") as file:
        return utl.pack_value(file.read())

def load_directory_structure(root, source):
    """load directory structure and convert it to list of (key, value) pairs"""
    pairs = []
    for current, dirs, files in os.walk(root):
        key = utl.unpack_key(root, current, source)
        if key != None:
            value = ""
            count = len(files)
            if count == 0:
                # no value
                pass
            elif count == 1:
                # there is a value
                value = load_value(os.path.join(current, files[0]))
            else:
                raise ValueError("expected at most 1 file in {0}, "
                                 "got {1} instead".format(current, count))
            pairs.append((key, value))
    return pairs


def unpack(dump, root, source, log=None):
    """unpack zeke dump file into directory structure"""
    count = 0
    with open(dump, "r") if dump is not "-" else sys.stdin as f:
        for line in f:
            count = count + 1
            (key, value) = utl.unpack_pair(line)
            level = len(key.split(os.sep))
            indent = "  " * level
            subkey = utl.strip_source_subpath(key, source)
            dir = os.path.join(root, subkey)
            #print("{2}creating directory '{0}' for key {1}".format(dir, key, indent), file=sys.stderr)
            mkpath(dir)
            if value:
                basename = utl.key_filename(subkey, source)
                outfile = os.path.join(dir, basename)
                if log is not None:
                    print("{2}saving value of '{0}' to '{1}'".format(key,
                                                                     outfile,
                                                                     indent),
                          file=log)
                with open(outfile, "w") as vf:
                    vf.write(utl.unpack_value(value))
    if log is not None:
        print("nodes processed: {0}".format(count), file=log)

def pack(root, dump, source, log=None):
    """pack directory structure into zeke dump file"""
    pairs = load_directory_structure(root, source)
    if log is not None:
        map(lambda x: print("updating node {0}".format(x[0]), file=log), pairs)
    with open(dump, "w") if dump is not "-" else sys.stdout as f:
        f.write(utl.pack_pairs(pairs))
    if log is not None:
        print("nodes processed: {0}".format(len(pairs)), file=log)
