def defaultify(value,default):
    """Return `default` if `value` is `None`. Otherwise, return `value`"""
    if None == value:
        return default
    else:
        return value

def defaultifyDict(dictionary,key,default):
    """Return `default` if either `key` is not in `dictionary`, or `dictionary[key]` is `None`. Otherwise, return `dictionary[key]`"""
    if key in dictionary:
        return defaultify(dictionary[key],default)
    else:
        return default
