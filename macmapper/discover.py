from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.errind import RequestTimedOut
import logging
from .exception import SnmpException

oids = {
    'sysDescr': '.1.3.6.1.2.1.1.1.0',
    'sysName':  '.1.3.6.1.2.1.1.5.0'
}

cmdGen = cmdgen.AsynCommandGenerator()

def discover_host(host, community, timeout, retries, callback, ctx):  
  cmdGen.getCmd(
      cmdgen.CommunityData(community),
      cmdgen.UdpTransportTarget((host, 161), timeout=timeout, retries=retries),
      (oids['sysDescr'], oids['sysName']),
      (callback, ctx)
  )

def discover_callback(handle, errorIndication, errorStatus, errorIndex, varBinds, ctx):
  if isinstance(errorIndication, RequestTimedOut):
    logging.debug('discover_callback: {}@{} timed out'.format(ctx['community'], ctx['address']))
    return
  if errorIndication:
    raise SnmpException(errorIndication)
  if errorStatus:
    raise SnmpException(errorStatus)

  logging.debug('discover_callback: {}@{} responded'.format(ctx['community'], ctx['address']))

  # append is thread-safe
  ctx['discovered'].append({
    'address': ctx['address'],
    'community': ctx['community'],
    'sysDescr': str(varBinds[0][1]),
    'sysName': str(varBinds[1][1]),
  })

def dedup_hosts(hosts):
  unique_hosts = {host['address']: host for host in hosts}
  return unique_hosts.values()

def discover_hosts(hosts, communities, timeout=0.5, retries=0):
  discovered = []
  for host in hosts:
    for community in communities:
      logging.debug('discover_hosts: Trying {}@{}'.format(community, host))
      ctx = {
        'address': host,
        'community': community,
        'discovered': discovered
      }
      discover_host(host, community, timeout, retries, discover_callback, ctx)
  cmdGen.snmpEngine.transportDispatcher.runDispatcher()
  return dedup_hosts(discovered)

