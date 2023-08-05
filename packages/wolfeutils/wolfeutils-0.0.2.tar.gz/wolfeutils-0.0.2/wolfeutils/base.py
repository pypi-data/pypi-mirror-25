import bz2
import contextlib
import gzip
import string
import sys


def openFunc(fname, mode='r'):
    '''Open a file with apprproiate open compression function.'''
    if fname.endswith('.gz'):
        opener = gzip.open
    elif fname.endswith('.bz2'):
        opener = bz2.decompress
    else:
        opener = open
    return opener(fname, mode)


@contextlib.contextmanager
def smart_open(filename=None, mode='r', stream=sys.stdin):
    '''If filename is a name string, open a handle with possible compression.
       If it is reserved '-' or None, treat it as an IO stream. Available stream
       optiosn are sys.stdin, sys.stdout, or sys.stderr.'''
    if filename and 'endswith' in dir(filename) and filename != '-':
        fhandle = openFunc(filename, mode)
    else:
        fhandle = stream
    try:
        yield fhandle
    finally:
        if fhandle is not sys.stdout:
            fhandle.close()


def fileslug(name):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in name if c in valid_chars)
