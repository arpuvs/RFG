#-----------------------------------------------------------------------------
# Name:        GPIBObject.py
# Purpose:     This module defines the base GPIBObject class and provides
#              simple functionality to scan for connected instruments
#
# Author:      Tom MacLeod
#
# Created:     2006/10/26
# RCS-ID:      $Id: GPIBObject.py 353 2013-10-17 21:05:30Z kshresth $
# Revisions:   Added NO_EQUIP (no equipment) debug mode / local equipment feature - Kaushal Shrestha
#              Added the generic GPIB Object functions. - Kaushal Shrestha
#-----------------------------------------------------------------------------

import time, visa
from NO_EQUIP.__ADI_GPIB_DEBUG__ import *

def GetAllGPIBDevices(rm):
    ilist = rm.list_resources()
    rlist = []
    for rname in ilist:
        if 'GPIB' in rname:
            i = rm.open_resource(rname)
            name = i.query('*IDN?')
            rlist.append((rname,name))
    return rlist

class GPIBObjectBaseClass(object):
    def __init__(self, name, addr=-1, delay=0.25):
        rm = visa.ResourceManager()
        if addr == -1: #Find first instrument
            namelist = GetAllGPIBDevices(rm)
            self.instr = None
            for rname,id in namelist:
                if id.lower().startswith(name.lower()):
                    self.instr = rm.open_resource(rname)
            if not self.instr:
                raise ValueError('GPIB Device: "'+name+'" Not Found')
        else:
            self.instr = rm.open_resource('GPIB0::' + str(addr))
        self.__SetDelay__(delay)

    def Query(self, command):
        '''Queries the instrument with the SCPI command'''
        return self.instr.query(command)

    def Read(self, command):
        raise Exception("Not implemented")

    def Write(self, command):
        '''Sends the SCPI command to the instrument'''
        self.instr.write(command)
        time.sleep(self.__delay__)

    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d

    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__

    Delay = property(__GetDelay__, __SetDelay__, None, "Gets/Sets Instrument Delay")