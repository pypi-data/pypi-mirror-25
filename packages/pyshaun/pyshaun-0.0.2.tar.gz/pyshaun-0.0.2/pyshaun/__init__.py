__version__ = '0.0.2'
__all__ = [ 'load', 'load_file', 'dump' ]

from .decoder import SHAUNDecoder

def load_file(fp, **kwargs):
    try:
        f = open(str(fp), 'r')
        return load(f.read(), **kwargs)
    except:
        return load(fp.read(), **kwargs)

def load(s, **kwargs):
    dec = SHAUNDecoder(s, **kwargs)
    return dec.decode()

def dump(sn):
    return SHAUNPP(sn).encode()
