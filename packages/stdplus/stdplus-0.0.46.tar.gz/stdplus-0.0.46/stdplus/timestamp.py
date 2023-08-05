from epoch import epoch

def timestamp(dt):
    return (dt - epoch).total_seconds()    
