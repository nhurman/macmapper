import logging
from . import snmp
from . import device

def Switch(host, community):
    sw = device.Switch()

    # Switch
    oids = {v: k for (k, v) in sw.props.items()}
    values = snmp.get(host, community, *oids)
    values = {oids[str(key.getOid())]: val for (key, val) in values.items()}
    sw.values = snmp.to_scalar(values)

    # Ports
    p = device.Port()
    oids = {v: k for (k, v) in p.props.items()}
    values = snmp.bulk(host, community, *oids)

    ports = {}
    for (key, value) in values.items():
      bits = str(key.getOid()).split('.')
      k = '.'.join(bits[:-1])
      if k not in oids:
        logging.error('Unknown key k={}; key={}; value={}'.format(k, key, value))
        continue
      name = oids[k]
      index = int(bits[-1])
      if index not in ports:
        ports[index] = device.Port()
      ports[index].values[name] = value

    for p in ports.values():
      p.apply_types()
      p.values = snmp.to_scalar(p.values)
    
    sw.ports = ports
    return sw