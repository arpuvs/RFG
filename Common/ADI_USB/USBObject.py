import visa

def GetAllUSBVISADevices(rm):
    import visa
    ilist = rm.list_resources()
    rlist = [] 
    for rname in ilist:
        if 'USB' in rname:
            i = rm.open_resource(rname)
            name = i.query('*IDN?')
            rlist.append((rname,name))
    return rlist

class USBObjectBaseClass(object):
    def __init__(self, name, addr = None, getall=True):
        rm = visa.ResourceManager()
        if addr is None:
            namelist = GetAllUSBVISADevices(rm)
            self.instr = None
            for rname, id in namelist:                
                if id.lower().startswith(name.lower()):
                    self.instr = rm.open_resource(rname)
            if not self.instr:
                raise ValueError('USB Device: "' + name + '" Not Found')
        else:
            self.instr = rm.open_resource('USB0::'+addr)