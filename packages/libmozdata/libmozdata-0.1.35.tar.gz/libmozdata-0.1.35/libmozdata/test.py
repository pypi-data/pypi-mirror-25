from .hgmozilla import Annotate
from pprint import pprint

path = 'netwerk/protocol/http/nsHttpConnectionMgr.cpp'
info = Annotate.get(path)

pprint(info)
