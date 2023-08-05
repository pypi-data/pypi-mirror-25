def readfile(filename):
    """Read contents of file specified by `filename`"""
    f = open(filename,'r')
    s = f.read()
    f.close()
    return s
