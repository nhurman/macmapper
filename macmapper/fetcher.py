from pysnmp.entity.rfc3413.oneliner import cmdgen
from .exception import SnmpException

def get_mac_table(host, community):
  oid = '.1.3.6.1.2.1.17.7.1.2.2.1.2'

  cmdGen = cmdgen.CommandGenerator()  
  errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
      cmdgen.CommunityData(community),
      cmdgen.UdpTransportTarget((host, 161)),
      0, 25,
      oid
  )

  if errorIndication:
    raise SnmpException(errorIndication)
  if errorStatus:
    raise SnmpException(errorStatus)

  mac_table = []
  for varBindTableRow in varBindTable:
    for name, val in varBindTableRow:
      bits = str(name.getOid())[len(oid):].split('.')
      vlan = bits.pop(0)
      address = ':'.join(['{0:02x}'.format(int(x)) for x in bits])

      mac_table.append({
        'port': int(val),
        'vlan': int(vlan),
        'mac':  address
      })
  return mac_table
