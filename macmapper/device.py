import inspect
import json

# http://stackoverflow.com/questions/4241171/inspect-python-class-attributes
def get_user_attributes(cls):
  boring = dir(type('dummy', (object,), {}))
  return dict([item
          for item in inspect.getmembers(cls)
          if item[0] not in boring])

class Item:
  def __init__(self):
    self.indexed = False
    self.props = {}
    self.types = {}
    self.values = {}
  
  def __str__(self):
    return self.values['name']
  
  def __repr__(self):
    return '{}({})'.format(self.__class__.__name__, self.__str__())
  
  def apply_types(self):
    for (key, val) in self.types.items():
      if key in self.values:
        self.values[key] = val(self.values[key])
  
  def json(self):
    return json.dumps(self.values)

class Switch(Item):
  def __init__(self):
    super().__init__()
    self.ports = []
    self.props = {
      'descr'        : '1.3.6.1.2.1.1.1.0',
      'uptime'       : '1.3.6.1.2.1.1.3.0',
      'contact'      : '1.3.6.1.2.1.1.4.0',
      'name'         : '1.3.6.1.2.1.1.5.0',
      'location'     : '1.3.6.1.2.1.1.6.0',
    }
  
  def json(self):
    v = dict(self.values)
    v['ports'] = {k: p.values for (k, p) in self.ports.items()}
    return json.dumps(v)

class Port(Item):
  def __init__(self):
    super().__init__()
    self.indexed = True
    self.props = {
      'descr'        : '1.3.6.1.2.1.2.2.1.2',
      'mtu'          : '1.3.6.1.2.1.2.2.1.4',
    # 'speed'        : '1.3.6.1.2.1.2.2.1.5',
      'admin_status' : '1.3.6.1.2.1.2.2.1.7',
      'oper_status'  : '1.3.6.1.2.1.2.2.1.8',
      'last_change'  : '1.3.6.1.2.1.2.2.1.9',
      'in_octets'    : '1.3.6.1.2.1.2.2.1.10',
      'in_errors'    : '1.3.6.1.2.1.2.2.1.14',
      'out_octets'   : '1.3.6.1.2.1.2.2.1.16',
      'out_errors'   : '1.3.6.1.2.1.2.2.1.20',

      'name'         : '1.3.6.1.2.1.31.1.1.1.1',
      'in_octets'    : '1.3.6.1.2.1.31.1.1.1.6',
      'in_uni_pkts'  : '1.3.6.1.2.1.31.1.1.1.7',
      'in_mul_pkts'  : '1.3.6.1.2.1.31.1.1.1.8',
      'in_brd_pkts'  : '1.3.6.1.2.1.31.1.1.1.9',
      'out_octets'   : '1.3.6.1.2.1.31.1.1.1.10',
      'out_uni_pkts' : '1.3.6.1.2.1.31.1.1.1.11',
      'out_mul_pkts' : '1.3.6.1.2.1.31.1.1.1.12',
      'out_brd_pkts' : '1.3.6.1.2.1.31.1.1.1.13',
      'speed'        : '1.3.6.1.2.1.31.1.1.1.15',
      'alias'        : '1.3.6.1.2.1.31.1.1.1.18',
    }
    self.types = {
      'admin_status' : PortStatus,
      'oper_status'  : PortStatus
    }

class PortStatus:
  UP = 1
  DOWN = 2
  TESTING = 3
  UNKNOWN = 4
  DORMANT = 5
  NOT_PRESENT = 6
  LOWER_DOWN = 7

  def __init__(self, status):
    self.status = status

  def __str__(self):   
    str_attrs = {v:k for (k, v) in get_user_attributes(self.__class__).items()}
    if self.status not in str_attrs:
      return str(self.status)
    return str_attrs[self.status]

  def __repr__(self):   
    return 'PortStatus({})'.format(self.__str__())
  