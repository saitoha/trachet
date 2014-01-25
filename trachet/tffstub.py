
import logging

try:
    import ctff as tff
    if not tff.signature == "febb6c52a3e1d52fe530f887fbdd975f":
        raise ImportError('Fail to validate signature hash of TFF library.')
except ImportError, e:
    logging.exception(e)
    from tff import tff
