from pprint import pprint
import logging
import macmapper

FORMAT = '%(asctime)-15s|%(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

switches = macmapper.discover.discover_hosts(
    ('10.252.2.210',),
    ('public', 'mapper-test',),
    timeout=0.5, retries=1
)

"""
pprint(switches)

mac_tables = {}
for switch in switches:
  mac_tables[switch['address']] = macmapper.fetcher.get_mac_table(switch['address'], switch['community'])

pprint(mac_tables)
"""

for switch in switches:
  sw = macmapper.builder.Switch(switch['address'], switch['community'])
  mac = macmapper.fetcher.get_mac_table(switch['address'], switch['community'])
  print(sw)
  for p in sw.ports.values():
    print(p)
  for m in mac:
    m['port'] = str(sw.ports[m['port']]) + ' ' + sw.ports[m['port']].values['alias']
  
  pprint(mac)