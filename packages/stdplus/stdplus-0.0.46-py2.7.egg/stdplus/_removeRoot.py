from __future__ import print_function

import os
import platform

def removeRoot(filename):
    assert(not platform.system() == "Windows") # This will not work on Windows since it has drive specifications
    if os.path.isabs(filename):
        return filename[1:]
    return filename
