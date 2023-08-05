from _atomicCount import AtomicCount
from _readfile import readfile
from _sshConfig import *
from _writefile import writefile
from _fexecvp import fexecvp
from _fnmatches import fnmatches
from _removeRoot import removeRoot
from _run_cmd import *
from _defaultify import *
from _isInt import *
from epoch import epoch
from timestamp import timestamp

import re

__all__ = [
    'AtomicCount',
    'contains',
    'defaultify',
    'defaultify',
    'defaultifyDict',
    'defaultifyDict',
    'elipsifyMiddle',
    'epoch',
    'fexecvp',
    'fnmatches',
    'getSshHost',
    'isInt',
    'isIp',
    'keyscanHost',
    'readSshConfig',
    'readfile',
    'removeKnownHosts',
    'removeRoot',
    'resetKnownHost',
    'resetKnownHosts',
    'run',
    'run_cmd',
    'timestamp',
    'writefile'
]

def contains(small, big):
    for i in xrange(len(big)-len(small)+1):
        for j in xrange(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False

def isIp(string):
    return None != re.match("^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",string)

def elipsifyMiddle(s, n):
    if len(s) <= n:
        # string is already short-enough
        return s
    # half of the size, minus the 3 .'s
    n_2 = int(n) / 2 - 3
    # whatever's left
    n_1 = n - n_2 - 3
    return '{0}...{1}'.format(s[:n_1], s[-n_2:])
