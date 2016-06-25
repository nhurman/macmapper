from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1902 import TimeTicks
from pysnmp.proto.rfc1905 import EndOfMibView
import datetime
from .exception import SnmpException

def bulk(host, community, *oids):
  cmdGen = cmdgen.CommandGenerator()
  errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
      cmdgen.CommunityData(community),
      cmdgen.UdpTransportTarget((host, 161)),
      0, 25,
      *oids
  )

  if errorIndication:
    raise SnmpException(errorIndication)
  if errorStatus:
    raise SnmpException(errorStatus)

  ret = {}
  for varBindTableRow in varBindTable:
    for name, val in varBindTableRow:
      if not isinstance(val, EndOfMibView):
        ret[name] = val
  return ret

def walk(host, community, *oids):
  cmdGen = cmdgen.CommandGenerator()
  errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
      cmdgen.CommunityData(community),
      cmdgen.UdpTransportTarget((host, 161)),
      *oids
  )

  if errorIndication:
    raise SnmpException(errorIndication)
  if errorStatus:
    raise SnmpException(errorStatus)

  ret = {}
  for varBindTableRow in varBindTable:
    for name, val in varBindTableRow:
      if not isinstance(val, EndOfMibView):
        ret[name] = val
  return ret

def get(host, community, *oids):
  cmdGen = cmdgen.CommandGenerator()  
  errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.getCmd(
      cmdgen.CommunityData(community),
      cmdgen.UdpTransportTarget((host, 161)),
      *oids
  )

  if errorIndication:
    raise SnmpException(errorIndication)
  if errorStatus:
    raise SnmpException(errorStatus)

  ret = {}
  for name, val in varBindTable:
    if not isinstance(val, EndOfMibView):
      ret[name] = val
  return ret

def to_scalar(values):
  ret = {}
  for (name, value) in values.items():
    if isinstance(value, TimeTicks):
      value = str(datetime.timedelta(seconds=int(value)/100.))
    elif not isinstance(value, bool):
      try:
        value = int(value)
      except (ValueError, TypeError):
        value = str(value)
    if not isinstance(name, str):
      name = str(name.getOid())
    ret[name] = value
  return ret