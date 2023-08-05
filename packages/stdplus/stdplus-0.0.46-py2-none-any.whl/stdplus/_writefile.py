def writefile(filename,contents):
    """Write `contents` to file specified by `filename`"""
    f = open(filename,'w')
    f.write(contents)
    f.close()
